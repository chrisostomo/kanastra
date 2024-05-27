FROM python:3.9

# Instalações e configurações do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Criação de usuário não privilegiado
RUN useradd --create-home --shell /bin/bash celeryuser

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Criação do diretório de logs e ajuste de permissões
RUN mkdir -p /app/logs && chown -R celeryuser:celeryuser /app/logs

# Alterar para o usuário não privilegiado
USER celeryuser

# Comando padrão (pode ser sobrescrito no docker-compose.yml)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
