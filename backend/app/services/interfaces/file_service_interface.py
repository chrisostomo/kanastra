from abc import ABC, abstractmethod
from app.schemas import CsvFileCreate, CsvFile, DebtCreate
from typing import List

class IFileService(ABC):
    @abstractmethod
    def save_csv_file(self, file_create: CsvFileCreate) -> CsvFile:
        pass

    @abstractmethod
    def list_files(self) -> List[CsvFile]:
        pass

    @abstractmethod
    def process_csv_task(self, file_path: str, email: str, csv_file_id: int) -> dict:
        pass
