import React, { createContext, useReducer, useContext, useEffect } from 'react';

// Tipos
type FileContextState = {
  isLoading: boolean;
  file: File | null;
  fileList: File[];
  error: string | null;
};

type FileAction =
  | { type: 'SET_LOADING'; payload: { isLoading: boolean } }
  | { type: 'SET_FILE'; payload: { file: File | null } }
  | { type: 'SET_FILE_LIST'; payload: { fileList: File[] } }
  | { type: 'SET_ERROR'; payload: { error: string | null } };

type FileProviderProps = { children: React.ReactNode };

// Estado Inicial
const initialState: FileContextState = {
  isLoading: false,
  file: null,
  fileList: [],
  error: null,
};

// Reducer
const fileReducer = (state: FileContextState, action: FileAction): FileContextState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload.isLoading };
    case 'SET_FILE':
      return { ...state, file: action.payload.file, isLoading: false };
    case 'SET_FILE_LIST':
      return { ...state, fileList: action.payload.fileList, isLoading: false };
    case 'SET_ERROR':
      return { ...state, error: action.payload.error, isLoading: false };
    default:
      return state;
  }
};

// Contexto
const FileContext = createContext<FileContextState | undefined>(undefined);
const FileDispatchContext = createContext<React.Dispatch<FileAction> | undefined>(undefined);

const useFileContext = (): { state: FileContextState, uploadFile: (formData: FormData) => Promise<void> } => {
  const state = useContext(FileContext);
  const dispatch = useContext(FileDispatchContext);

  if (!state || !dispatch) {
    throw new Error('useFileContext must be used within a FileProvider');
  }

  const fetchFiles = async () => {
    dispatch({ type: 'SET_LOADING', payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/files`);
      const data = await response.json();
      dispatch({ type: 'SET_FILE_LIST', payload: { fileList: data } });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: { error: (error as Error).message } });
    }
  };

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8080/ws');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'FILE_LIST_UPDATED') {
        fetchFiles().catch(console.error);
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  const uploadFile = async (formData: FormData) => {
    dispatch({ type: 'SET_LOADING', payload: { isLoading: true } });
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      dispatch({ type: 'SET_FILE', payload: { file: data } });
      await fetchFiles();
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: { error: (error as Error).message } });
    }
  };

  return {
    state,
    uploadFile
  };
};

const FileProvider: React.FC<FileProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  return (
    <FileContext.Provider value={state}>
      <FileDispatchContext.Provider value={dispatch}>
        {children}
      </FileDispatchContext.Provider>
    </FileContext.Provider>
  );
};

export { FileProvider, useFileContext };
