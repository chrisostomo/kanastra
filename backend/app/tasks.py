from celery import Celery
import os
import csv
from database import SessionLocal
import models

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_file_task(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            db = SessionLocal()
            for row in reader:
                debt = models.Debt(
                    name=row['name'],
                    government_id=row['governmentId'],
                    email=row['email'],
                    debt_amount=float(row['debtAmount']),
                    debt_due_date=row['debtDueDate'],
                    debt_id=row['debtId']
                )
                db.add(debt)
            db.commit()
        return {"status": "success", "message": "File processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def save_file(file_content, file_name, directory='uploads'):
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")

def send_email(email):
    # Placeholder para enviar email
    pass
