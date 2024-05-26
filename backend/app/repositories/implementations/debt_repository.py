from sqlalchemy.orm import Session
from app.models.debt import Debt
from app.schemas import DebtCreate, Debt
from app.repositories.interfaces.debt_repository_interface import IDebtRepository

class DebtRepository(IDebtRepository):
    def __init__(self, db: Session):
        self.db = db

    def bulk_create(self, debts: List[DebtCreate]) -> None:
        db_debts = [Debt(**debt.dict()) for debt in debts]
        self.db.bulk_save_objects(db_debts)
        self.db.commit()

    def update(self, debt: Debt) -> Debt:
        db_debt = self.db.query(Debt).filter(Debt.id == debt.id).one()
        db_debt.boleto_generated = debt.boleto_generated
        db_debt.boleto_sent = debt.boleto_sent
        db_debt.new_due_date = debt.new_due_date
        self.db.commit()
        self.db.refresh(db_debt)
        return db_debt
