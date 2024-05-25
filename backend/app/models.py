import os
from sqlalchemy import Column, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'debts'

    debt_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    government_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    debt_amount = Column(Float)
    debt_due_date = Column(Date)
import os
from sqlalchemy import create_engine
from app.models import Base

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()

