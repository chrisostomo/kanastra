import React, { useEffect, useContext } from 'react';
import { FileContext } from '../context/FileContext';
import axios from 'axios';

const FileList = () => {
  const context = useContext(FileContext);

  if (!context) {
    throw new Error('FileList must be used within a FileProvider');
  }

  const { state, dispatch } = context;
  const { files, loading, error } = state;

  useEffect(() => {
    const fetchFiles = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        const response = await axios.get('http://localhost:8080/files');
        const transformedFiles = Object.entries(response.data.tasks).map(([key, value]) => ({
          name: key,
          status: value
        }));
        dispatch({ type: 'SET_FILES', payload: transformedFiles });
      } catch (error) {
        const errorMsg = error.response?.data?.message || error.message || 'Erro ao carregar os arquivos.';
        dispatch({ type: 'SET_ERROR', payload: errorMsg });
      } finally {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    fetchFiles();
    const intervalId = setInterval(fetchFiles, 5000); // Atualiza a cada 5 segundos

    return () => clearInterval(intervalId); // Limpa o intervalo ao desmontar o componente
  }, [dispatch]);

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4 text-center text-blue-500">
        Lista de Tarefas
      </h1>
      {loading && <div className="mb-4 text-blue-500">Carregando...</div>}
      {error && <div className="mb-4 text-red-500">{error}</div>}
      {!loading && !error && Array.isArray(files) && (
        <ul className="w-full max-w-md">
          {files.map((file, index) => (
            <li key={index} className="p-2 border-b border-gray-300">
              {file.name}: {file.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FileList;
