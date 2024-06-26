from celery import Celery
import os
from app.models.db import SessionLocal  # Verifique se o caminho está correto
from app.factories.create_file_service import create_file_service  # Verifique se o caminho está correto

CELERY_BROKER_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.update(
    broker_connection_retry_on_startup=True  # Atualização da configuração para manter o comportamento
)

@celery.task
def process_csv_task(file_path: str, email: str, csv_file_id: int):
    db = SessionLocal()
    file_service = create_file_service(db)
    result = file_service.process_csv_task(file_path, email, csv_file_id)
    db.close()
    return result
