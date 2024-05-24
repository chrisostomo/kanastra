import React, { createContext, useReducer, ReactNode, Dispatch } from 'react';

// Definir tipos para o estado
interface File {
  name: string;
  // Adicione outros campos conforme necessário
}

interface FileState {
  files: File[];
  loading: boolean;
  error: string | null;
}

// Estado inicial
const initialState: FileState = {
  files: [],
  loading: false,
  error: null
};

// Definir tipos para as ações
type FileAction =
  | { type: 'ADD_FILE'; payload: File }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'SET_FILES'; payload: File[] };

// Criar o contexto
const FileContext = createContext<FileContextProps | undefined>(undefined);

interface FileContextProps {
  state: FileState;
  dispatch: Dispatch<FileAction>;
}

// Reducer para manipular ações
function fileReducer(state: FileState, action: FileAction): FileState {
  switch (action.type) {
    case 'ADD_FILE':
      return { ...state, files: [...state.files, action.payload] };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_FILES':
      return { ...state, files: action.payload, loading: false };
    default:
      return state;
  }
}

// Provider componente
export const FileProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  return (
    <FileContext.Provider value={{ state, dispatch }}>
      {children}
    </FileContext.Provider>
  );
};

export { FileContext };
