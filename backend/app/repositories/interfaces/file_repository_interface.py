from abc import ABC, abstractmethod
from app.schemas import CsvFileCreate, CsvFile
from typing import List

class IFileRepository(ABC):
    @abstractmethod
    def create(self, file_create: CsvFileCreate) -> CsvFile:
        pass

    @abstractmethod
    def list_files(self) -> List[CsvFile]:
        pass

    @abstractmethod
    def update_status(self, csv_file_id: int, status: str, error_message: str = None) -> CsvFile:
        pass
