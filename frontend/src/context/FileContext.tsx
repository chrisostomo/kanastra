import React, { createContext, useReducer, ReactNode, Dispatch, useContext } from 'react';
import axios from 'axios';

interface File {
  name: string;
  taskId: string;
}

interface Task {
  id: string;
  status: string;
  message: string;
}

interface FileState {
  files: File[];
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

const initialState: FileState = {
  files: [],
  tasks: [],
  loading: false,
  error: null
};

type FileAction =
  | { type: 'ADD_FILE'; payload: File }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'SET_FILES'; payload: File[] }
  | { type: 'SET_TASKS'; payload: Task[] };

const FileContext = createContext<{ state: FileState; dispatch: Dispatch<FileAction> } | undefined>(undefined);

const fileReducer = (state: FileState, action: FileAction): FileState => {
  switch (action.type) {
    case 'ADD_FILE':
      return { ...state, files: [...state.files, action.payload] };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_FILES':
      return { ...state, files: action.payload, loading: false };
    case 'SET_TASKS':
      return { ...state, tasks: action.payload, loading: false };
    default:
      return state;
  }
};

export const FileProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  return (
    <FileContext.Provider value={{ state, dispatch }}>
      {children}
    </FileContext.Provider>
  );
};

export const useFileContext = () => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useFileContext must be used within a FileProvider');
  }
  return context;
};
