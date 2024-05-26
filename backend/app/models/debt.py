from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Debt(Base):
    __tablename__ = 'debts'

    id = Column(Integer, primary_key=True, index=True)
    debt_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    government_id = Column(String, index=True)
    email = Column(String, index=True)
    debt_amount = Column(Float)
    debt_due_date = Column(DateTime)
    csv_file_id = Column(Integer, ForeignKey('csv_files.id'))

    csv_file = relationship("CsvFile", back_populates="debts")
