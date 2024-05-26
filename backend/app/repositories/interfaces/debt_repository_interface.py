from abc import ABC, abstractmethod
from app.schemas import DebtCreate, Debt
from typing import List

class IDebtRepository(ABC):
    @abstractmethod
    def bulk_create(self, debts: List[DebtCreate]) -> None:
        pass

    @abstractmethod
    def update(self, debt: Debt) -> Debt:
        pass
