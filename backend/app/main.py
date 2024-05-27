import os
from fastapi import FastAPI
from .controllers import file_controller
from .exceptions.error_handler import init_error_handlers
import logging

logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir, exist_ok=True)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "app.log")),
        logging.StreamHandler()
    ]
)
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
