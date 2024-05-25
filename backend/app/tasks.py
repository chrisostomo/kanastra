from celery import Celery
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Debt
import smtplib
from email.mime.text import MIMEText
from .redis_client import RedisClient

app = Celery('app.tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TaskProcessor:
    def __init__(self, redis_client: RedisClient, session_factory):
        self.redis_client = redis_client
        self.session_factory = session_factory

    def process_csv_task(self, file_path, email):
        session = self.session_factory()
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                batch = []
                for row in reader:
                    debt = Debt(
                        name=row['name'],
                        government_id=row['governmentId'],
                        email=row['email'],
                        debt_amount=float(row['debtAmount']),
                        debt_due_date=row['debtDueDate'],
                        debt_id=row['debtId']
                    )
                    batch.append(debt)
                    if len(batch) >= 100:  # Process in batches of 100
                        session.bulk_save_objects(batch)
                        session.commit()
                        batch = []
                if batch:  # Process remaining records
                    session.bulk_save_objects(batch)
                    session.commit()
            self.redis_client.complete_task(email)
            self.send_email(email)
            return {"status": "success", "message": "File processed successfully"}
        except Exception as e:
            session.rollback()
            task_id = f"task:{email}"
            self.redis_client.client.set(task_id, "failed")
            raise Exception(f"Failed to process CSV: {e}")
        finally:
            session.close()

    def send_email(self, email):
        try:
            msg = MIMEText("Your CSV file has been processed.")
            msg['Subject'] = "CSV Processing Complete"
            msg['From'] = "no-reply@example.com"
            msg['To'] = email

            with smtplib.SMTP('smtp.example.com') as server:
                server.login('username', 'password')
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")

def save_file(file_content, file_name, directory='uploads'):
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")

task_processor = TaskProcessor(redis_client=RedisClient(), session_factory=SessionLocal)

@app.task
def process_csv_task(file_path, email):
    return task_processor.process_csv_task(file_path, email)
