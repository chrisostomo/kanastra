from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from pydantic import ValidationError
from app.exceptions import CsvFileProcessingError
import logging

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

async def csv_file_processing_error_handler(request: Request, exc: CsvFileProcessingError):
    logger.error(f"CSV Processing Error: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

def init_error_handlers(app):
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(CsvFileProcessingError, csv_file_processing_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
