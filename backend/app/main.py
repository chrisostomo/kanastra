from fastapi import FastAPI
from app.controllers import file_controller
from app.exceptions.error_handler import init_error_handlers
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("logs/app.log"),
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(file_controller.router)

init_error_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
