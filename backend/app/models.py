from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'debts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    governmentId = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    debtAmount = Column(Numeric(10, 2), nullable=False)
    debtDueDate = Column(Date, nullable=False)
    debtID = Column(String(36), nullable=False)
