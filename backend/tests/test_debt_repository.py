import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models.debt import Debt
from app.repositories.implementations.debt_repository import DebtRepository
from app.schemas import DebtCreate

@pytest.fixture
def session():
    return MagicMock(spec=Session)

@pytest.fixture
def debt_repository(session):
    return DebtRepository(session)

def test_bulk_create(debt_repository, session):
    debts = [DebtCreate(name="John Doe", government_id="11111111111", email="johndoe@kanastra.com.br", debt_amount=1000000.00, debt_due_date="2022-10-01", csv_file_id=1)]
    debt_repository.bulk_create(debts)
    session.bulk_save_objects.assert_called()
    session.commit.assert_called()

def test_update_debt(debt_repository, session):
    debt = Debt(id=1, name="John Doe", government_id="11111111111", email="johndoe@kanastra.com.br", debt_amount=1000000.00, debt_due_date="2022-10-01", csv_file_id=1)
    debt_repository.update(debt)
    session.query(Debt).filter.assert_called()
    session.commit.assert_called()
    session.refresh.assert_called()
