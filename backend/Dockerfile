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
RUN pip install pytest pytest-asyncio pymysql

# Exposição da porta 8080
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
