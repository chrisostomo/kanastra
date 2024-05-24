# Documentação da API

## Descrição Geral
Esta documentação detalha os endpoints disponíveis na API, métodos suportados, parâmetros de entrada, e exemplos de uso. A API é projetada para facilitar o upload e o processamento de arquivos CSV, assim como a recuperação de informações sobre as dívidas processadas.

## Endpoints

### 1. Upload de Arquivo CSV
- **Endpoint**: `/upload`
- **Método**: POST
- **Parâmetros**:
    - `file` (multipart/form-data): Arquivo CSV a ser enviado.
    - `email` (form-data): Endereço de email para notificações.
- **Resposta de Sucesso**:
    - **Código**: 201
    - **Conteúdo**: `{ "message": "File uploaded and processing started" }`
- **Resposta de Erro**:
    - **Código**: 400
    - **Conteúdo**: `{ "detail": "Invalid file format" }`
- **Descrição**: Permite o upload de arquivos CSV para processamento. O arquivo deve ter a extensão `.csv`.

### 2. Obter Dados de Arquivos
- **Endpoint**: `/files`
- **Método**: GET
- **Parâmetros**: Nenhum
- **Resposta de Sucesso**:
    - **Código**: 200
    - **Conteúdo**: Lista de objetos `Debt`
- **Descrição**: Retorna uma lista de todas as dívidas processadas disponíveis no banco de dados.

## Exemplos de Uso

### Upload de Arquivo
```javascript
const uploadFile = async (file, email) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('email', email);

  try {
    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload file.');
    }

    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Exemplo de uso:
// uploadFile(fileInput.files[0], 'user@example.com');
