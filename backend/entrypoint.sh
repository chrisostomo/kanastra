#!/bin/bash
# entrypoint.sh

# Aplicar migrações do Alembic
alembic upgrade head

# Iniciar o servidor FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8080
