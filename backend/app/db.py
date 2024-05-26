import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Erro ao configurar o banco de dados: {e}")
    raise

def init_db() -> None:
    """
    Cria as tabelas do banco de dados, se elas ainda não existirem.
    """
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if 'debts' not in tables:
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso.")
        else:
            print("Tabelas já existem.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        raise