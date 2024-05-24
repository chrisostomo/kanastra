from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Debt
from .schemas import DebtCreate
from .tasks import process_csv
import os

app = FastAPI()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.post("/upload")
async def upload_file(file: UploadFile, email: str = Form(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format")
    contents = await file.read()
    process_csv.delay(contents.decode("utf-8"), email)
    return JSONResponse(status_code=201, content={"message": "File uploaded and processing started"})

@app.get("/files")
def get_files():
    session = SessionLocal()
    debts = session.query(Debt).all()
    session.close()
    return debts
