
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
    ```bash
    git clone https://github.com/your-repo/kanasta
    cd kanasta
    ```

2. **Configuração do Backend**:
    - Navegue até o diretório `backend`:
      ```bash
      cd backend
      ```
    - Construa e inicie os containers Docker:
      ```bash
      docker-compose up --build
      ```

3. **Configuração do Frontend**:
    - Navegue até o diretório `frontend`:
      ```bash
      cd ../frontend
      ```
    - Instale as dependências:
      ```bash
      npm install
      ```
    - Inicie o servidor de desenvolvimento:
      ```bash
      npm run dev
      ```

### Uso

1. **Upload de Arquivo**:
   - Acesse o formulário de upload de arquivos em `http://localhost:8888`.
   - Selecione um arquivo CSV e faça o upload.

2. **Visualizar Arquivos Carregados**:
   - Navegue até a página de listagem de arquivos para ver todos os arquivos carregados e seus status.

### Estrutura do Projeto

```
kanasta/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── tasks.py
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   └── package.json
├── README.md
```

### Testes

- **Testes Unitários e de Integração**: Certifique-se de que todos os testes estejam passando executando:
  ```bash
  cd backend
  pytest tests/unit
  pytest tests/integration
  ```

## Contribuindo

Contribuições são bem-vindas! Por favor, faça um fork do repositório e crie um pull request com suas alterações.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Agradecimentos

Agradecemos aos colaboradores e à comunidade de código aberto pelos valiosos recursos e ferramentas.

---

Com essa configuração, você pode gerenciar uploads de arquivos de forma eficiente, processá-los de forma assíncrona e manter um registro histórico, garantindo um sistema robusto e escalável. Bom desenvolvimento!
