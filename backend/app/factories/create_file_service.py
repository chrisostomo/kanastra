from sqlalchemy.orm import Session
from app.repositories.implementations.file_repository import FileRepository
from app.repositories.implementations.debt_repository import DebtRepository
from app.services.implementations.file_service import FileService

def create_file_service(db: Session) -> FileService:
    file_repository = FileRepository(db)
    debt_repository = DebtRepository(db)
    return FileService(file_repository, debt_repository)
