# README da Aplicação de Cobrança

## Visão Geral
Este projeto consiste em uma aplicação completa de cobrança, incluindo frontend e backend. O frontend é construído usando React, enquanto o backend é desenvolvido com FastAPI e utiliza WebSockets para atualizações em tempo real. A aplicação permite o upload de arquivos CSV contendo informações de dívida e atualiza a lista de arquivos em tempo real.

## Estrutura do Projeto

```bash
/kanastra-challenge-boilerplate
  /frontend
    /src
      /components
        /ui
          file-provider.tsx
          file-uploader.tsx
          index.ts
          layout.tsx
          no-match.tsx
          table.tsx
      /pages
        FileListPage.tsx
        FileUploadPage.tsx
      /reducers
        fileReducer.ts
      /tests
        FileUploadPage.test.tsx
        FileListPage.test.tsx
      /types
        index.ts
    index.html
    jest.config.js
    jest.setup.js
    package.json
    tsconfig.json
    vite.config.ts
  /backend
    /app
      /controllers
        file_controller.py
      /exceptions
        error_handler.py
        __init__.py
      /factories
        create_file_service.py
      /logs
        app.log
      /models
        db.py
        file.py
        debt.py
      /repositories
        /interfaces
          file_repository_interface.py
          debt_repository_interface.py
        /implementations
          file_repository.py
          debt_repository.py
      /services
        /interfaces
          file_service_interface.py
        /implementations
          file_service.py
      /websocket_manager
        websocket_manager.py
      main.py
      schemas.py
      tasks.py
      utils.py
    alembic.ini
    Dockerfile
    requirements.txt
    tests/
      test_file_service.py
      test_file_repository.py
      test_debt_repository.py
  docker-compose.yml
  README.md
```

## Instruções de Instalação

### Requisitos
- Docker
- Git

### Configuração do Ambiente
1. Clone o repositório:
    ```sh
    git clone https://github.com/chrisostomo/kanastra.git
    cd kanastra
    ```

2. Construa e inicie os contêineres Docker:
    ```sh
    docker-compose up --build
    ```

A aplicação estará disponível em:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

### Testes

#### Backend
Para executar os testes no backend, use:
```sh
docker-compose exec backend pytest
```

#### Frontend
Para executar os testes no frontend, use:
```sh
docker-compose exec front npm test
# ou
docker-compose exec front yarn test
```

## Uso dos Princípios SOLID
- **Single Responsibility Principle (SRP):** Cada classe e módulo tem uma única responsabilidade. Por exemplo, `FileRepository` é responsável por operações de banco de dados relacionadas a arquivos, enquanto `FileService` lida com a lógica de negócios para arquivos.
- **Open/Closed Principle (OCP):** As classes estão abertas para extensão, mas fechadas para modificação. Podemos estender as funcionalidades de serviços ou repositórios sem alterar as implementações existentes.
- **Liskov Substitution Principle (LSP):** As classes derivadas podem ser usadas como substitutas para suas classes base sem alterar o comportamento desejado. Por exemplo, `IFileRepository` e `IDebtRepository` são interfaces que podem ter múltiplas implementações.
- **Interface Segregation Principle (ISP):** Interfaces específicas são criadas para diferentes responsabilidades, evitando interfaces inchadas.
- **Dependency Inversion Principle (DIP):** O código de alto nível não depende de detalhes de implementação de baixo nível, mas de abstrações. Por exemplo, `FileService` depende de `IFileRepository` e `IDebtRepository`, e não de suas implementações concretas.

## Manipulação de Erros
O backend utiliza manipuladores de erros personalizados definidos em `app/exceptions/error_handler.py`. Diferentes tipos de exceções são tratados e logados de maneira apropriada. Erros de validação, erros de processamento de arquivos CSV e exceções genéricas são tratados e retornam respostas JSON detalhadas.

## Micro Serviços
A aplicação é projetada como micro serviços, com cada serviço tendo sua própria responsabilidade. O backend é dividido em vários componentes, cada um lidando com aspectos específicos da aplicação, como gerenciamento de arquivos, dívidas e comunicação via WebSocket.

## Processamento em Fila
O processamento de arquivos CSV é gerenciado em segundo plano usando Celery e RabbitMQ. Tarefas de processamento são enviadas para a fila e executadas assíncronamente, permitindo que a aplicação continue responsiva enquanto grandes volumes de dados são processados.

## Documentação da API
A documentação da API é gerada automaticamente pelo FastAPI e está disponível nos seguintes endpoints:

- Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentação ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Contribuição
Sinta-se à vontade para contribuir com o projeto. Para isso, faça um fork do repositório, crie uma nova branch para sua feature ou correção e abra um Pull Request.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
