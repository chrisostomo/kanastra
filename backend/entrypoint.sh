#!/bin/bash
# entrypoint.sh

# Função para verificar se o MySQL está pronto
function mysql_ready(){
    python << END
import sys
import pymysql
try:
    conn = pymysql.connect(
        host="${DB_HOST}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        database="${DB_NAME}",
        port=int("${DB_PORT}")
    )
except pymysql.err.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

# Esperar o MySQL iniciar
until mysql_ready; do
    echo 'Waiting for MySQL...'
    sleep 2
done

# Aplicar migrações do Alembic
alembic upgrade head || true

# Iniciar o servidor FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8080