#!/bin/bash

# Criando a estrutura de diretórios
mkdir -p project-root/frontend/public project-root/frontend/src project-root/backend

# Criando o Dockerfile do Frontend (React)
cat << 'EOF' > project-root/frontend/Dockerfile
# Use the official React image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Serve the React app
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose port 3000
EXPOSE 3000
EOF

# Criando o Dockerfile do Backend (Go)
cat << 'EOF' > project-root/backend/Dockerfile
# Use the official Golang image
FROM golang:1.16

# Set the working directory
WORKDIR /app

# Copy go.mod and go.sum
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application
RUN go build -o main .

# Run the Go application
CMD ["./main"]

# Expose port 8080
EXPOSE 8080
EOF

# Criando o docker-compose.yml
cat << 'EOF' > project-root/docker-compose.yml
version: '3.8'

services:
  front:
    build:
      context: ./frontend
    container_name: frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
    environment:
      - REACT_APP_API_URL=http://api:8080

  api:
    build:
      context: ./backend
    container_name: backend
    ports:
      - "8080:8080"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_USER=root
      - DB_PASSWORD=example
      - DB_NAME=kanastra

  db:
    image: mysql:5.7
    container_name: database
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=example
      - MYSQL_DATABASE=kanastra
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
EOF

# Criando o arquivo .env
cat << 'EOF' > project-root/.env
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=example
DB_NAME=kanastra
REACT_APP_API_URL=http://api:8080
EOF

echo "Estrutura do projeto e arquivos criados com sucesso!"
