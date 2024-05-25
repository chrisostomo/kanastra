import React, { useState } from 'react';
import { useFileContext } from '../context/FileContext';
import axios from 'axios';

const FileUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const { dispatch } = useFileContext();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      await axios.post('http://localhost:8080/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      dispatch({ type: 'SET_LOADING', payload: false });
      // Opcional: fetchFiles() aqui para atualizar a lista após o upload
    } catch (error) {
      const errorMsg = error.response?.data?.message || error.message || 'Erro ao carregar o arquivo.';
      dispatch({ type: 'SET_ERROR', payload: errorMsg });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center p-4">
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">
        Enviar CSV
      </button>
    </form>
  );
};

export default React.memo(FileUploader);
