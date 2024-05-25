import React, { useState, useContext } from 'react';
import { FileContext } from '../context/FileContext';
import axios from 'axios';

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const { dispatch } = useContext(FileContext);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8080/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      dispatch({ type: 'SET_LOADING', payload: true });
      // Opcional: fetchFiles() aqui para atualizar a lista após o upload
    } catch (error) {
      const errorMsg = error.response?.data?.message || error.message || 'Erro ao carregar o arquivo.';
      dispatch({ type: 'SET_ERROR', payload: errorMsg });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center p-4">
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">Enviar CSV</button>
    </form>
  );
};

export default FileUploader;
