# Utiliza a imagem base oficial do Uvicorn-Gunicorn-FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . /app

# Instala as dependências de teste e outros pacotes adicionais
RUN pip install pytest pytest-asyncio pymysql alembic python-dotenv

# Exposição da porta 8080
EXPOSE 8080

# Adiciona as variáveis de ambiente do arquivo .env
COPY .env /app/

# Executa as migrações antes de iniciar a aplicação
CMD ["bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
