FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta de depuração
EXPOSE 8080
EXPOSE 5678

# Adiciona /app ao PYTHONPATH
ENV PYTHONPATH=/app

# Define o comando para iniciar a aplicação com suporte para depuração
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
