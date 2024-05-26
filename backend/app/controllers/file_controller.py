from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.db import SessionLocal
from app.schemas import CsvFileCreate, CsvFile
from app.tasks import process_csv_task
from app.websocket_manager.websocket_manager import WebSocketManager
from app.factories.create_file_service import create_file_service
from app.utils import save_file

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", status_code=202, response_model=CsvFile)
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile, email: str, db: Session = Depends(get_db)):
    """
    Faz o upload de um arquivo CSV para processamento.

    - **file**: O arquivo CSV a ser enviado.
    - **email**: O e-mail do usuário que está fazendo o upload.
    """
    file_service = create_file_service(db)
    try:
        contents = await file.read()
        csv_file_create = CsvFileCreate(filename=file.filename)
        csv_file = file_service.save_csv_file(csv_file_create)
        task_id, file_path = save_file(contents, file.filename)
        background_tasks.add_task(process_csv_task, file_path=file_path, email=email, csv_file_id=csv_file.id)

        await WebSocketManager().broadcast(f"File {file.filename} uploaded and processing started")
        return csv_file
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files", response_model=List[CsvFile])
async def list_files(db: Session = Depends(get_db)):
    """
    Retorna a lista de arquivos CSV enviados.
    """
    file_service = create_file_service(db)
    return file_service.list_files()
