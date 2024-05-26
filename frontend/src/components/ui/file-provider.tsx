import React, { createContext, useReducer, useContext, useEffect } from 'react';
import { fileReducer, initialState } from '@/reducers';
import { FileProviderProps, FileContextType, FileActionType } from '@/types';

const FileContext = createContext<FileContextType | undefined>(undefined);

export const useFileContext = (): FileContextType => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useFileContext must be used within a FileProvider');
  }
  return context;
};

const FileProvider: React.FC<FileProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8080/ws'); // Altere para o URL do seu WebSocket

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'FILE_LIST_UPDATED') {
        fetchFiles();
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  const fetchFiles = async () => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/files`);
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE_LIST, payload: { fileList: data, isLoading: false } });
    } catch (error) {
      dispatch({ type: FileActionType.SET_ERROR, payload: { error: (error as Error).message, isLoading: false } });
    }
  };

  const uploadFile = async (formData: FormData) => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE, payload: { file: data } });
      fetchFiles();
    } catch (error) {
      dispatch({ type: FileActionType.SET_ERROR, payload: { error: (error as Error).message, isLoading: false } });
    }
  };

  const value = {
    state,
    dispatch,
    fetchFiles,
    uploadFile,
  };

  return <FileContext.Provider value={value}>{children}</FileContext.Provider>;
};

export default FileProvider;
