#!/bin/sh

# Espera pelo banco de dados estar disponível
while ! nc -z db 3306; do
  echo 'Waiting for the database...'
  sleep 2
done

# Inicializa o banco de dados e inicia o servidor
python /app/app/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8080
