
# Sistema de Upload e Gerenciamento de Arquivos Kanasta

## Visão Geral

Este projeto é uma aplicação full-stack projetada para gerenciar uploads de arquivos e manter um histórico atualizado dos arquivos carregados. A aplicação consiste em uma API backend construída com FastAPI e um frontend desenvolvido utilizando React e TypeScript. O sistema permite que os usuários façam upload de arquivos CSV, que são então processados e listados em uma tabela para fácil visualização e gerenciamento.

## Funcionalidades

### Backend
- **Upload de Arquivos**: A API pode receber arquivos CSV através de uma requisição POST.
- **Processamento em Fila**: Arquivos carregados são enviados para uma fila de processamento assíncrono.
- **Notificação por Email**: Após a conclusão do processamento, um email é enviado ao usuário que carregou o arquivo.
- **Integração com Banco de Dados**: Arquivos e seus metadados são armazenados em um banco de dados MySQL.
- **Fila Redis**: Utiliza Redis para gerenciar tarefas em segundo plano.

### Frontend
- **Formulário de Upload de Arquivos**: Um formulário para fazer upload de arquivos CSV.
- **Listagem de Arquivos**: Uma tabela que lista todos os arquivos carregados, atualizada em tempo real conforme novos arquivos são carregados.
- **React Context API**: Gerencia o estado entre componentes de maneira eficiente.
- **Design Responsivo**: Garante usabilidade em diferentes dispositivos.

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Para construção dos endpoints da API.
- **Celery**: Para gerenciamento de tarefas assíncronas.
- **Redis**: Como broker de mensagens para o Celery.
- **MySQL**: Banco de dados para armazenar metadados dos arquivos.
- **Docker**: Containeriza a aplicação para fácil implantação.

### Frontend
- **React**: Para construção das interfaces de usuário.
- **TypeScript**: Adiciona segurança de tipos ao JavaScript.
- **Tailwind CSS**: Para estilização da aplicação.
- **Vite**: Uma ferramenta de build que proporciona uma experiência de desenvolvimento mais rápida e leve para projetos web modernos.

## Começando

### Pré-requisitos
- Docker e Docker Compose
- Node.js e npm

### Instalação

1. **Clone o repositório**:
    \`\`\`bash
    git clone https://github.com/chrisostomo/kanastra
    cd kanastra
    \`\`\`

2. **Configuração do Backend e Frontend**:
    - Construa e inicie os containers Docker:
      \`\`\`bash
      docker-compose up --build
      \`\`\`

3. **Configuração do Frontend**:
    - Navegue até o diretório \`frontend\`:
      \`\`\`bash
      cd frontend
      \`\`\`
    - Instale as dependências:
      \`\`\`bash
      npm install
      \`\`\`
    - Inicie o servidor de desenvolvimento:
      \`\`\`bash
      npm run dev
      \`\`\`

### Uso

1. **Upload de Arquivo**:
   - Acesse o formulário de upload de arquivos em \`http://localhost:8888\`.
   - Selecione um arquivo CSV e faça o upload.

2. **Visualizar Arquivos Carregados**:
   - Navegue até a página de listagem de arquivos para ver todos os arquivos carregados e seus status.

### Estrutura do Projeto

\`\`\`
kanastra/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── tasks.py
│   ├── requirements.txt
│   └── tests/
│       ├── unit/
│       └── integration/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── README.md
\`\`\`

### Testes

- **Testes Unitários e de Integração**: Certifique-se de que todos os testes estejam passando executando:
  \`\`\`bash
  cd backend
  pytest tests/unit
  pytest tests/integration
  \`\`\`

### Integração Contínua (CI)

Este projeto utiliza GitHub Actions para integração contínua. O workflow de CI está definido no arquivo \`.github/workflows/ci.yml\`.

1. **Verificar Código**:
    - Toda vez que um push ou pull request é feito para a branch \`main\`, os testes são executados automaticamente.

2. **Arquivo de Workflow**:
    \`\`\`yaml
    name: CI

    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main

    jobs:
      test:
        runs-on: ubuntu-latest

        services:
          mysql:
            image: mysql:8.0
            env:
              MYSQL_ROOT_PASSWORD: example
              MYSQL_DATABASE: kanastra
            ports:
              - 3306:3306
            options: >-
              --health-cmd "mysqladmin ping --silent"
              --health-interval 10s
              --health-timeout 5s
              --health-retries 3
          redis:
            image: redis:6.2
            ports:
              - 6379:6379

        steps:
        - name: Checkout code
          uses: actions/checkout@v2

        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: 3.9

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r backend/requirements.txt

        - name: Add .env file to backend
          run: echo "${{ secrets.ENV_VARS }}" > backend/.env

        - name: Run tests
          env:
            REDIS_HOST: redis
            REDIS_PORT: 6379
            REDIS_DB: 0
            CELERY_BROKER_URL: redis://redis:6379/0
            CELERY_RESULT_BACKEND: redis://redis:6379/0
            DB_HOST: db
            DB_PORT: 3306
            DB_USER: root
            DB_PASSWORD: example
            DB_NAME: kanastra
            SMTP_SERVER: smtp.example.com
            SMTP_PORT: 587
            SMTP_USERNAME: username
            SMTP_PASSWORD: password
            SMTP_FROM_EMAIL: no-reply@example.com
          run: |
            docker-compose up -d
            pytest backend/tests
    \`\`\`

### Configurando Secrets no GitHub

Para que o arquivo \`.env\` seja criado corretamente durante a execução do workflow, você deve definir \`ENV_VARS\` nos secrets do seu repositório GitHub:

1. Vá para o repositório no GitHub.
2. Clique em **Settings**.
3. No menu lateral, clique em **Secrets and variables** e depois em **Actions**.
4. Clique no botão **New repository secret**.
5. Adicione um novo secret chamado \`ENV_VARS\` com o seguinte valor:

\`\`\`
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=example
DB_NAME=kanastra

SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=username
SMTP_PASSWORD=password
SMTP_FROM_EMAIL=no-reply@example.com
\`\`\`

Isso garantirá que as variáveis de ambiente necessárias estejam disponíveis para os testes de CI.
