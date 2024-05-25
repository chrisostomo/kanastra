from pydantic import BaseModel, EmailStr
from datetime import datetime

class DebtBase(BaseModel):
    name: str
    governmentId: str
    email: EmailStr
    debtAmount: int
    debtDueDate: datetime
    debtID: str

class DebtCreate(DebtBase):
    pass

class Debt(DebtBase):
    id: int

    class Config:
        orm_mode = True
