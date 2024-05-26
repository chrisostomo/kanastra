from app.repositories.interfaces.file_repository_interface import IFileRepository
from app.repositories.interfaces.debt_repository_interface import IDebtRepository
from app.schemas import CsvFileCreate, CsvFile, DebtCreate
from app.services.interfaces.file_service_interface import IFileService
from app.exceptions import CsvFileProcessingError
from typing import List
import csv
from datetime import datetime, timedelta

class FileService(IFileService):
    def __init__(self, file_repository: IFileRepository, debt_repository: IDebtRepository):
        self.file_repository = file_repository
        self.debt_repository = debt_repository

    def save_csv_file(self, file_create: CsvFileCreate) -> CsvFile:
        return self.file_repository.create(file_create)

    def list_files(self) -> List[CsvFile]:
        return self.file_repository.list_files()

    def process_csv_task(self, file_path: str, email: str, csv_file_id: int) -> dict:
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                debts = []
                for row in reader:
                    debt_create = DebtCreate(
                        name=row['name'],
                        government_id=row['governmentId'],
                        email=row['email'],
                        debt_amount=float(row['debtAmount']),
                        debt_due_date=datetime.strptime(row['debtDueDate'], '%Y-%m-%d'),
                        csv_file_id=csv_file_id
                    )
                    debts.append(debt_create)

            self.debt_repository.bulk_create(debts)
            self.file_repository.update_status(csv_file_id, 'success')

            # Aqui adicionamos lógica para gerar e enviar boletos
            for debt in debts:
                # Lógica para gerar o boleto
                debt.boleto_generated = True
                # Simulamos o envio do boleto
                debt.boleto_sent = True
                # Definimos uma nova data de vencimento
                debt.new_due_date = debt.debt_due_date + timedelta(days=30)
                self.debt_repository.update(debt)

            return {"status": "success", "message": "File processed successfully"}
        except Exception as e:
            self.file_repository.update_status(csv_file_id, 'error', str(e))
            raise CsvFileProcessingError(f"Error processing CSV file: {e}")
