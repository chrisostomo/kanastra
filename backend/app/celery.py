from celery import Celery

def make_celery(app_name=__name__) -> Celery:
    """
    Inicializa uma instância do Celery com Redis como broker e backend.
    """
    try:
        return Celery(app_name, broker='redis://redis:6379/0', backend='redis://redis:6379/0')
    except Exception as e:
        print(f"Erro ao inicializar o Celery: {e}")
        raise

# Inicializa o Celery
celery = make_celery()
