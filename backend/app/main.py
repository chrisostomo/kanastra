from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models, schemas
from crud import get_user, create_user, get_processed_files
from tasks import process_file_task, save_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        db_user = get_user(self.db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return create_user(db=self.db, user=user)

class FileService:
    def __init__(self, db: Session):
        self.db = db

    def process_file(self, file_path: str):
        task = process_file_task.delay(file_path)
        return {"task_id": task.id}

    def list_files(self):
        try:
            files = get_processed_files(self.db)
            return files
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)

@app.post("/process_file/")
async def process_file_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_content = await file.read()
        file_path = save_file(file_content, file.filename)
        file_service = FileService(db)
        return file_service.process_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/", response_model=List[schemas.File])
def list_files_endpoint(db: Session = Depends(get_db)):
    file_service = FileService(db)
    return file_service.list_files()
