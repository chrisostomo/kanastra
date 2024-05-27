from pydantic import BaseModel, EmailStr, condecimal, constr, validator
from datetime import datetime
from typing import Optional, List

class CsvFileBase(BaseModel):
    filename: str

class CsvFileCreate(CsvFileBase):
    pass

class CsvFileUpdate(BaseModel):
    status: str
    error_message: Optional[str] = None

class CsvFile(CsvFileBase):
    id: int
    uploaded_at: datetime
    status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class DebtBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    government_id: constr(strip_whitespace=True, min_length=11, max_length=11)
    email: EmailStr
    debt_amount: condecimal(gt=0)
    debt_due_date: datetime

    @validator('debt_due_date')
    def validate_due_date(cls, v):
        if v < datetime.now():
            raise ValueError('debt_due_date must be in the future')
        return v

class DebtCreate(DebtBase):
    csv_file_id: int

class Debt(DebtBase):
    id: int

    class Config:
        from_attributes = True
