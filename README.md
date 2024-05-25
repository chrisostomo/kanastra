
# Kanstra Application

[![Kanstra](https://img.shields.io/badge/Kanstra-FastAPI%20%7C%20Celery%20%7C%20React-blue)](https://github.com/chrisostomo/kanastra)

## Overview

Kanstra é uma aplicação que utiliza FastAPI para o backend, Celery para processamento assíncrono, SQLAlchemy para interação com o banco de dados, e Redis para gerenciamento de tarefas. O frontend é desenvolvido usando tecnologias modernas como React ou Vue.js (especificar conforme necessário).

## Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)

Cada módulo na aplicação tem uma responsabilidade única:

- **Backend**
  - **`app/main.py`**: Configura a aplicação FastAPI e define os endpoints.
  - **`app/service.py`**: Contém a lógica de negócios da aplicação.
  - **`app/db.py`**: Configura a conexão com o banco de dados usando SQLAlchemy.
  - **`app/models.py`**: Define os modelos de banco de dados.
  - **`app/redis_client.py`**: Gerencia operações com Redis.
  - **`app/task.py`**: Implementa tarefas assíncronas com Celery.

### Open/Closed Principle (OCP)

Os módulos estão abertos para extensão, mas fechados para modificação. Por exemplo:

- **`AppService`**: A classe de serviço pode ser estendida para adicionar novos métodos sem modificar o código existente.

### Liskov Substitution Principle (LSP)

As subclasses devem ser substituíveis por suas superclasses. Em Python, isso é mais informal, mas seguimos o princípio ao garantir que os objetos possam ser substituídos sem alterar o comportamento esperado.

### Interface Segregation Principle (ISP)

Segregamos as responsabilidades em classes e métodos específicos para evitar interfaces inchadas:

- **`AppService`**: Foca na lógica de negócios relacionada ao upload e recuperação de tarefas.
- **`RedisClient`**: Gerencia operações com Redis de forma isolada.

### Dependency Inversion Principle (DIP)

Utilizamos injeção de dependência para desacoplar as classes:

- **`AppService`** recebe dependências (`RedisClient` e `SessionLocal`) através do construtor, facilitando a testabilidade e manutenção.

## Estrutura do Projeto

```plaintext
kanstra/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── service.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── redis_client.py
│   │   ├── task.py
│   ├── entrypoint.sh
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── uploads/
│   └── testes/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   ├── public/
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── docker-compose.yml
└── README.md
```

## Configuração do Ambiente

### Requisitos

- Docker
- Docker Compose
- Python 3.8+
- Node.js 14+

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```plaintext
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
DB_NAME=<your_db_name>
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
SMTP_FROM_EMAIL=<your_smtp_email>
SMTP_SERVER=<your_smtp_server>
SMTP_PORT=<your_smtp_port>
SMTP_USERNAME=<your_smtp_username>
SMTP_PASSWORD=<your_smtp_password>
```

### Executando a Aplicação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/chrisostomo/kanastra
   cd kanstra
   ```

2. **Inicie os containers com Docker Compose:**

   ```bash
   docker-compose up --build
   ```

3. **Acesse a aplicação:**

   - Frontend: [http://localhost:8888](http://localhost:8888)
   - Backend: [http://localhost:8080](http://localhost:8080)

## Testes

### Backend

1. **Instale as dependências de teste no contêiner:**

   ```bash
   docker exec -it backend pip install -r requirements.txt
   docker exec -it backend pip install pytest httpx pytest-asyncio
   ```

2. **Execute os testes:**

   ```bash
   docker exec -it backend pytest
   ```

### Frontend

1. **Instale as dependências no contêiner:**

   ```bash
   docker exec -it frontend npm install
   ```

2. **Execute os testes:**

   ```bash
   docker exec -it frontend npm run test
   ```

## Contribuição

1. Fork o repositório.
2. Crie uma branch: `git checkout -b minha-branch`.
3. Faça suas alterações e commit: `git commit -m 'Minha alteração'`.
4. Envie para o repositório remoto: `git push origin minha-branch`.
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
