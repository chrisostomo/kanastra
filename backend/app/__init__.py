import os
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Inicializa o Celery
def make_celery(app_name=__name__):
    return Celery(app_name, broker='redis://redis:6379/0', backend='redis://redis:6379/0')

celery = make_celery()

# Configuração do banco de dados
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importa e inicializa os modelos (tabelas)
from .models import Base

def init_db():
    # Criação das tabelas
    Base.metadata.create_all(bind=engine)

# Inicialização do banco de dados
init_db()

# Configuração do Redis
from .redis_client import RedisClient
redis_client = RedisClient()
