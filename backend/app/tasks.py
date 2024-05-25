import os
import csv
import smtplib
from email.mime.text import MIMEText
from .celery import celery
from .redis_client import RedisClient
from .db import SessionLocal
from .models import Debt

class TaskProcessor:
    def __init__(self, redis_client: RedisClient, session_factory):
        """
        Inicializa a classe TaskProcessor com um cliente Redis e uma fábrica de sessões.

        Args:
            redis_client (Redis): O cliente Redis.
            session_factory (sessionmaker): A fábrica de sessões do SQLAlchemy.
        """
        self.redis_client = redis_client
        self.session_factory = session_factory

    def process_csv_task(self, file_path: str, email: str) -> dict:
        """
        Processa o arquivo CSV e salva os dados no banco de dados.

        Args:
            file_path (str): Caminho do arquivo CSV.
            email (str): Email do usuário.

        Returns:
            dict: Status e mensagem de sucesso ou falha.
        """
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
                    if len(batch) >= 100:  # Processar em lotes de 100
                        session.bulk_save_objects(batch)
                        session.commit()
                        batch = []
                if batch:  # Processar registros restantes
                    session.bulk_save_objects(batch)
                    session.commit()
            self.complete_task(email)
            self.send_email(email)
            return {"status": "success", "message": "File processed successfully"}
        except Exception as e:
            session.rollback()
            self.fail_task(email)
            raise Exception(f"Failed to process CSV: {e}")
        finally:
            session.close()

    def send_email(self, email: str) -> None:
        """
        Envia um email notificando que o processamento do CSV foi concluído.

        Args:
            email (str): Email do usuário.
        """
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
        """
        Marca uma tarefa como concluída no Redis.

        Args:
            email (str): O email associado à tarefa.
        """
        try:
            task_id = f"task:{email}"
            self.redis_client.set(task_id, 'completed')
        except Exception as e:
            raise Exception(f"Failed to complete task: {e}")

    def fail_task(self, email: str) -> None:
        """
        Marca uma tarefa como falhada no Redis.

        Args:
            email (str): O email associado à tarefa.
        """
        try:
            task_id = f"task:{email}"
            self.redis_client.set(task_id, 'failed')
        except Exception as e:
            raise Exception(f"Failed to fail task: {e}")

def save_file(file_content: bytes, file_name: str, directory: str = 'uploads') -> str:
    """
    Salva o conteúdo do arquivo no sistema de arquivos.

    Args:
        file_content (bytes): Conteúdo do arquivo.
        file_name (str): Nome do arquivo.
        directory (str): Diretório onde o arquivo será salvo.

    Returns:
        str: Caminho do arquivo salvo.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")

# Inicializa o RedisClient e o SessionLocal
redis_client = RedisClient()
task_processor = TaskProcessor(redis_client=redis_client, session_factory=SessionLocal)

@celery.task
def process_csv_task(file_path: str, email: str) -> dict:
    """
    Tarefa Celery para processar o arquivo CSV.

    Args:
        file_path (str): Caminho do arquivo CSV.
        email (str): Email do usuário.

    Returns:
        dict: Status e mensagem de sucesso ou falha.
    """
    return task_processor.process_csv_task(file_path, email)
