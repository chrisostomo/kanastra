import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models.file import CsvFile
from app.repositories.implementations.file_repository import FileRepository
from app.schemas import CsvFileCreate

@pytest.fixture
def session():
    return MagicMock(spec=Session)

@pytest.fixture
def file_repository(session):
    return FileRepository(session)

def test_create_file(file_repository, session):
    file_create = CsvFileCreate(filename="test.csv")
    file_repository.create(file_create)
    session.add.assert_called()
    session.commit.assert_called()
    session.refresh.assert_called()

def test_list_files(file_repository, session):
    file_repository.list_files()
    session.query(CsvFile).all.assert_called()

def test_update_status(file_repository, session):
    csv_file_id = 1
    status = "processed"
    file_repository.update_status(csv_file_id, status)
    session.query(CsvFile).filter.assert_called()
    session.commit.assert_called()
    session.refresh.assert_called()
