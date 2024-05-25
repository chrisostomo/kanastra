from sqlalchemy import Column, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'debts'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    government_id = Column(String, index=True)
    email = Column(String, index=True)
    debt_amount = Column(Float)
    debt_due_date = Column(Date)
    debt_id = Column(String, unique=True, index=True)
