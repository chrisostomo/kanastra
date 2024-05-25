from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Debt
from .schemas import DebtCreate
from .tasks import process_csv
import os
import shutil

app = FastAPI()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile, email: str = Form(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        process_csv.delay(file_path, email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start CSV processing: {e}")

    return JSONResponse(status_code=201, content={"message": "File uploaded and processing started"})

@app.get("/files")
def get_files(db: Session = Depends(get_db)):
    try:
        debts = db.query(Debt).all()
        return debts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve files: {e}")
