from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class CsvFile(Base):
    __tablename__ = 'csv_files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploaded_at = Column(DateTime)
    status = Column(String)
    error_message = Column(String, nullable=True)

    debts = relationship("Debt", back_populates="csv_file")
