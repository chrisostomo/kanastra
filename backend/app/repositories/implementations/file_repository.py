from typing import List
from sqlalchemy.orm import Session
from app.models.file import CsvFile
from app.schemas import CsvFileCreate
from app.repositories.interfaces.file_repository_interface import IFileRepository

class FileRepository(IFileRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, file_create: CsvFileCreate) -> CsvFile:
        csv_file = CsvFile(**file_create.dict())
        self.db.add(csv_file)
        self.db.commit()
        self.db.refresh(csv_file)
        return csv_file

    def list_files(self) -> List[CsvFile]:
        return self.db.query(CsvFile).all()

    def update_status(self, csv_file_id: int, status: str, error_message: str = None) -> CsvFile:
        csv_file = self.db.query(CsvFile).filter(CsvFile.id == csv_file_id).one()
        csv_file.status = status
        csv_file.error_message = error_message
        self.db.commit()
        self.db.refresh(csv_file)
        return csv_file
