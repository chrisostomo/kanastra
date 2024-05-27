import React, { createContext, useReducer, useContext, useEffect, ReactNode } from 'react';
import { FileActionType, FileContextState, FileAction, FileProviderProps, FileContextType } from '@/types/file';
import { initialState, fileReducer } from '@/reducers/fileReducer';

const FileContext = createContext<FileContextType | undefined>(undefined);

const FileProvider: React.FC<FileProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  const fetchFiles = async () => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/files`);
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE_LIST, payload: { fileList: data } });
    } catch (error) {
      dispatch({ type: FileActionType.SET_ERROR, payload: { error: (error as Error).message } });
    }
  };

  useEffect(() => {
    const connectWebSocket = () => {
      const socket = new WebSocket('ws://localhost:8000/ws');

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === 'file_uploaded') {
          fetchFiles();
        }
      };

      socket.onclose = () => {
        console.log('WebSocket closed. Reconnecting...');
        setTimeout(connectWebSocket, 1000);
      };
    };

    connectWebSocket();
  }, []);

  const uploadFile = async (formData: FormData) => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE, payload: { file: data } });
      await fetchFiles();
    } catch (error) {
      dispatch({ type: FileActionType.SET_ERROR, payload: { error: (error as Error).message } });
    }
  };

  return (
    <FileContext.Provider value={{ state, dispatch, fetchFiles, uploadFile }}>
      {children}
    </FileContext.Provider>
  );
};

const useFileContext = (): FileContextType => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useFileContext must be used within a FileProvider');
  }
  return context;
};

export { FileProvider, useFileContext };
