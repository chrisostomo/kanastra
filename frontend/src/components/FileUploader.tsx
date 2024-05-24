import React, { useState, useContext } from 'react';
import { FileContext } from '../context/FileContext';
import axios from 'axios';

interface FileResponse {
  name: string;
  // Adicione outros campos conforme necessário
}

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState<string>('');
  const [message, setMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const context = useContext(FileContext);

  if (!context) {
    throw new Error('FileUploader must be used within a FileProvider');
  }

  const { dispatch } = context;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleUpload = async () => {
    if (!file || !email) {
      setErrorMessage('Por favor, selecione um arquivo e insira seu e-mail.');
      return;
    }
    dispatch({ type: 'SET_LOADING', payload: true });
    setMessage(null);
    setErrorMessage(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('email', email);
      const response = await axios.post<FileResponse>('http://localhost:8000/upload', formData);
      dispatch({ type: 'ADD_FILE', payload: response.data });
      dispatch({ type: 'SET_LOADING', payload: false });
      setMessage('Arquivo enviado com sucesso!');
    } catch (error) {
      const errorMsg = error.response?.data?.message || error.message || 'Erro ao enviar o arquivo.';
      dispatch({ type: 'SET_ERROR', payload: errorMsg });
      dispatch({ type: 'SET_LOADING', payload: false });
      setErrorMessage(errorMsg);
    }
  };

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4 text-center text-blue-500">
        Vamos lá! Envie seu arquivo e seu e-mail. Prometemos que vai ser rapidinho!
      </h1>
      {message && <div className="mb-4 text-green-500">{message}</div>}
      {errorMessage && <div className="mb-4 text-red-500">{errorMessage}</div>}
      <input
        type="email"
        value={email}
        onChange={handleEmailChange}
        placeholder="Digite seu e-mail"
        className="mb-4 p-2 border border-gray-300 rounded w-full max-w-md"
      />
      <input
        type="file"
        onChange={handleFileChange}
        accept=".csv, application/vnd.ms-excel"
        className="mb-4 p-2 border border-gray-300 rounded w-full max-w-md"
      />
      <button
        onClick={handleUpload}
        className="p-2 bg-blue-500 text-white rounded hover:bg-blue-700 w-full max-w-md"
      >
        Enviar
      </button>
    </div>
  );
};

export default FileUploader;
