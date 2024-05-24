# Dockerfile for React (kanastra-challenge-front)

FROM node:18

# Define o diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos de dependências
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia o restante dos arquivos do projeto
COPY . .

# Exposição
EXPOSE 8888

# Comando para iniciar a aplicação
CMD ["npm", "run", "dev:node"]
