import React, { useEffect } from 'react';
import { useFileContext } from '../components/index';

const FileListPage: React.FC = () => {
  const { state, fetchFiles } = useFileContext();

  useEffect(() => {
    fetchFiles().catch(console.error);
  }, [fetchFiles]);

  return (
    <div className="container mx-auto p-4 text-center">
      <h1 className="text-2xl mb-4">Lista de Arquivos</h1>
      {state.isLoading ? (
        <p className="text-gray-600">Carregando...</p>
      ) : (
        <ul className="list-disc list-inside">
          {state.fileList.map((file) => (
            <li key={file.filename} className="text-left text-gray-800">{file.filename}</li>
          ))}
        </ul>
      )}
      {state.error && <p className="text-red-600">Erro: {state.error}</p>}
    </div>
  );
};

export default FileListPage;
