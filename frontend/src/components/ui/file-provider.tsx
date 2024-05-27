import React, { createContext, useReducer, useContext, useEffect, useCallback } from 'react';
import { FileActionType, FileProviderProps, FileContextType } from '@/types/file';
import { initialState, fileReducer } from '@/reducers/fileReducer';
import { MESSAGES } from '@/constants/messages';

const FileContext = createContext<FileContextType | undefined>(undefined);

const FileProvider: React.FC<FileProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  const fetchFiles = useCallback(async () => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/files`);
      if (!response.ok) {
        throw new Error(MESSAGES.ERROR.FETCH_FILES + response.statusText);
      }
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE_LIST, payload: { fileList: data } });
    } catch (error) {
      //dispatch({ type: FileActionType.SET_ERROR, payload: { error: error.message } });
    }
  }, []);

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
        console.log(MESSAGES.ERROR.WEBSOCKET);
        setTimeout(connectWebSocket, 1000);
      };

      socket.onerror = (error) => {
        console.error(MESSAGES.ERROR.WEBSOCKET, error);
        dispatch({ type: FileActionType.SET_ERROR, payload: { error: MESSAGES.ERROR.WEBSOCKET } });
      };
    };

    connectWebSocket();
  }, [fetchFiles]);

  const uploadFile = useCallback(async (formData: FormData) => {
    dispatch({ type: FileActionType.SET_LOADING, payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(MESSAGES.ERROR.UPLOAD_FILE + response.statusText);
      }
      const data = await response.json();
      dispatch({ type: FileActionType.SET_FILE, payload: { file: data } });
      await fetchFiles();
    } catch (error) {
      //dispatch({ type: FileActionType.SET_ERROR, payload: { error: error.message } });
    }
  }, [fetchFiles]);

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
