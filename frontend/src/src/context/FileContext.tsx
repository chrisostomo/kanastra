// src/context/FileContext.tsx
import React, { createContext, useReducer, useContext } from 'react';

// Tipos de ações para gerenciar o estado
const ActionTypes = {
  SET_FILES: 'SET_FILES',
  ADD_FILE: 'ADD_FILE',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR'
};

// Estado inicial
const initialState = {
  files: [],
  loading: false,
  error: ''
};

// Criando o contexto
const FileContext = createContext({});

// Reducer para atualizar o estado
function fileReducer(state, action) {
  switch (action.type) {
    case ActionTypes.SET_FILES:
      return { ...state, files: action.payload, loading: false };
    case ActionTypes.ADD_FILE:
      return { ...state, files: [...state.files, action.payload], loading: false };
    case ActionTypes.SET_LOADING:
      return { ...state, loading: action.payload };
    case ActionTypes.SET_ERROR:
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}

// Provider que envolve seus componentes
export const FileProvider = ({ children }) => {
  const [state, dispatch] = useReducer(fileReducer, initialState);

  return (
    <FileContext.Provider value={{ state, dispatch }}>
      {children}
    </FileContext.Provider>
  );
};

// Hook personalizado para usar o contexto
export const useFile = () => useContext(FileContext);

export default FileContext;
