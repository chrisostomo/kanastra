import os
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .redis_client import RedisClient
from .main import create_app

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

# Configuração do banco de dados
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Erro ao configurar o banco de dados: {e}")
    raise

# Configuração do Redis
try:
    redis_client = RedisClient()
except Exception as e:
    print(f"Erro ao configurar o Redis: {e}")
    raise

def init_db() -> None:
    """
    Cria as tabelas do banco de dados.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        raise

# Inicialização do banco de dados
init_db()

# Criação da aplicação FastAPI
app = create_app()
