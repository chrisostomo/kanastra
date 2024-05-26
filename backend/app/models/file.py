from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .db import Base
import datetime

class CsvFile(Base):
    __tablename__ = 'csv_files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='processing')
    error_message = Column(String, nullable=True)

    debts = relationship("Debt", back_populates="csv_file")
