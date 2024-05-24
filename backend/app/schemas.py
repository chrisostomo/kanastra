from pydantic import BaseModel

class DebtCreate(BaseModel):
    name: str
    governmentId: str
    email: str
    debtAmount: float
    debtDueDate: str
    debtID: str
