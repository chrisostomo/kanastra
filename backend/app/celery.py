from celery import Celery
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

def make_celery(app_name=__name__) -> Celery:
    """
    Inicializa uma instância do Celery com Redis como broker e backend.

    Args:
        app_name (str): Nome da aplicação.

    Returns:
        Celery: Instância do Celery configurada.
    """
    try:
        broker_url = os.getenv('CELERY_BROKER_URL')
        backend_url = os.getenv('CELERY_RESULT_BACKEND')
        return Celery(app_name, broker=broker_url, backend=backend_url)
    except Exception as e:
        print(f"Erro ao inicializar o Celery: {e}")
        raise

# Inicializa o Celery
celery = make_celery()
