import pytest
from unittest.mock import MagicMock
from app.services.implementations.file_service import FileService
from app.schemas import CsvFileCreate, DebtCreate
from app.exceptions import CsvFileProcessingError

@pytest.fixture
def file_repository():
    return MagicMock()

@pytest.fixture
def debt_repository():
    return MagicMock()

@pytest.fixture
def file_service(file_repository, debt_repository):
    return FileService(file_repository, debt_repository)

def test_save_csv_file(file_service, file_repository):
    file_create = CsvFileCreate(filename="test.csv")
    file_service.save_csv_file(file_create)
    file_repository.create.assert_called_once_with(file_create)

def test_list_files(file_service, file_repository):
    file_service.list_files()
    file_repository.list_files.assert_called_once()

def test_process_csv_task(file_service, file_repository, debt_repository):
    file_path = "test.csv"
    email = "test@example.com"
    csv_file_id = 1

    with open(file_path, 'w') as f:
        f.write("name,governmentId,email,debtAmount,debtDueDate,debtId\n")
        f.write("John Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-01,1")

    file_service.process_csv_task(file_path, email, csv_file_id)

    file_repository.update_status.assert_called()
    debt_repository.bulk_create.assert_called()
