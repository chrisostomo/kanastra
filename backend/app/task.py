import os
import csv
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .celery import celery
from .redis_client import RedisClient
from .db import SessionLocal
from .models import Debt

app = FastAPI()

class Task:
    def __init__(self, redis_client: RedisClient, session_factory: Session):
        self.redis_client = redis_client
        self.session_factory = session_factory

    def process_csv_task(self, file_path: str, email: str) -> dict:
        session = self.session_factory()
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            # Extrair IDs governamentais para verificar duplicatas em lote
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

            self.complete_task(email)
            self.send_email(email)
            return {"status": "success", "message": "File processed successfully"}
        except IntegrityError as e:
            session.rollback()
            self.fail_task(email)
            raise Exception(f"Failed to process CSV due to IntegrityError: {e}")
        except Exception as e:
            session.rollback()
            self.fail_task(email)
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

    def complete_task(self, email: str) -> None:
        try:
            task_id = f"task:{email}"
            self.redis_client.set(task_id, 'completed')
        except Exception as e:
            raise Exception(f"Failed to complete task: {e}")

    def fail_task(self, email: str) -> None:
        try:
            task_id = f"task:{email}"
            self.redis_client.set(task_id, 'failed')
        except Exception as e:
            raise Exception(f"Failed to fail task: {e}")

def save_file(file_content: bytes, file_name: str, directory: str = 'uploads') -> str:
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")

redis_client = RedisClient()
task = Task(redis_client=redis_client, session_factory=SessionLocal)

@celery.task
def process_csv_task(file_path: str, email: str) -> dict:
    return task.process_csv_task(file_path, email)

@app.post("/uploadfile/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...), email: str = Form(...)):
    try:
        contents = await file.read()
        file_path = save_file(contents, file.filename)
        background_tasks.add_task(process_csv_task, file_path=file_path, email=email)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))