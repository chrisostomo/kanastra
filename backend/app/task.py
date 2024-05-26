import os
import csv
import smtplib
from email.mime.text import MIMEText
from fastapi import BackgroundTasks, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .celery import celery
from .redis_client import RedisClient
from .db import SessionLocal
from .models import Debt

class AppService:
    def __init__(self, redis_client: RedisClient, session_factory: Session):
        self.redis_client = redis_client
        self.session_factory = session_factory

    def process_csv_task(self, file_path: str, email: str) -> dict:
        session = self.session_factory()
        task_id = self.redis_client.create_task(email)
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            government_ids = [row['governmentId'] for row in rows]
            existing_ids = session.query(Debt.government_id).filter(Debt.government_id.in_(government_ids)).all()
            existing_ids = set([eid[0] for eid in existing_ids])

            batch = []
            for row in rows:
                if row['governmentId'] not in existing_ids:
                    debt = {
                        "debt_id": row['debtId'],
                        "name": row['name'],
                        "government_id": row['governmentId'],
                        "email": row['email'],
                        "debt_amount": float(row['debtAmount']),
                        "debt_due_date": row['debtDueDate']
                    }
                    batch.append(debt)
                    existing_ids.add(row['governmentId'])
                if len(batch) >= 100:
                    session.bulk_insert_mappings(Debt, batch)
                    session.commit()
                    batch = []
            if batch:
                session.bulk_insert_mappings(Debt, batch)
                session.commit()

            self.redis_client.complete_task(task_id)
            try:
                self.send_email(email)
            except Exception as e:
                self.redis_client.set(f'{task_id}_message', f'Processed but failed to send email: {e}')
            return {"status": "success", "message": "File processed successfully"}
        except IntegrityError as e:
            session.rollback()
            self.redis_client.fail_task(task_id)
            raise Exception(f"Failed to process CSV due to IntegrityError: {e}")
        except Exception as e:
            session.rollback()
            self.redis_client.fail_task(task_id)
            raise Exception(f"Failed to process CSV: {e}")
        finally:
            session.close()

    def send_email(self, email: str) -> None:
        try:
            msg = MIMEText("Your CSV file has been processed.")
            msg['Subject'] = "CSV Processing Complete"
            msg['From'] = os.getenv('SMTP_FROM_EMAIL')
            msg['To'] = email

            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))
            smtp_user = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")

    async def upload_csv(self, background_tasks: BackgroundTasks, email: str, file: UploadFile):
        try:
            contents = await file.read()
            file_path = save_file(contents, file.filename)
            background_tasks.add_task(process_csv_task, file_path=file_path, email=email)
            return {"filename": file.filename}, 202
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_tasks(self):
        tasks = self.redis_client.get_all_tasks()
        return TasksResponse(tasks=tasks), 200

def save_file(file_content: bytes, file_name: str, directory: str = 'uploads') -> str:
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")

@celery.task
def process_csv_task(file_path: str, email: str) -> dict:
    service = AppService(redis_client=RedisClient(), session_factory=SessionLocal)
    return service.process_csv_task(file_path, email)