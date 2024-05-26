import { FileActionType, FileContextState, FileAction } from '@/types';

// Estado inicial do contexto de arquivos
const initialState: FileContextState = {
  isLoading: false,
  file: null,
  fileList: [],
  error: null,
};

// Implementação do reducer
const fileReducer = (state: FileContextState, action: FileAction): FileContextState => {
  switch (action.type) {
    case FileActionType.SET_LOADING:
      return { ...state, isLoading: action.payload?.isLoading ?? false };
    case FileActionType.SET_FILE:
      return { ...state, file: action.payload?.file ?? null, isLoading: false };
    case FileActionType.SET_FILE_LIST:
      return { ...state, fileList: action.payload?.fileList ?? [], isLoading: false };
    case FileActionType.SET_ERROR:
      return { ...state, error: action.payload?.error ?? null, isLoading: false };
    default:
      return state;
  }
};

export { fileReducer, initialState };
