from sqlalchemy import Column, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'debts'

    debt_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), index=True)
    government_id = Column(String(20), unique=True, index=True)
    email = Column(String(100), index=True)
    debt_amount = Column(Float)
    debt_due_date = Column(Date)

    def __repr__(self):
        return f"<Debt(name={self.name}, email={self.email}, debt_amount={self.debt_amount})>"