from celery import Celery
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Debt
import smtplib
from email.mime.text import MIMEText
import os

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery.task
def process_csv(file_path, email):
    session = SessionLocal()
    try:
        with open(file_path, 'r') as file:
            csv_input = csv.reader(file)
            batch = []
            for row in csv_input:
                if row:
                    debt = Debt(
                        name=row[0],
                        governmentId=row[1],
                        email=row[2],
                        debtAmount=row[3],
                        debtDueDate=row[4],
                        debtID=row[5]
                    )
                    batch.append(debt)
                    if len(batch) >= 100:  # Process in batches of 100
                        session.bulk_save_objects(batch)
                        session.commit()
                        batch = []
            if batch:  # Process remaining records
                session.bulk_save_objects(batch)
                session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to process CSV: {e}")
    finally:
        session.close()

    send_email(email)

def send_email(email):
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
