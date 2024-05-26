import { ReactNode } from "react";

// Definição dos tipos de ações possíveis
export enum FileActionType {
  SET_LOADING = 'SET_LOADING',
  SET_FILE = 'SET_FILE',
  SET_FILE_LIST = 'SET_FILE_LIST',
  SET_ERROR = 'SET_ERROR',
}

// Definição da interface para uma ação do reducer
type ReducerAction<T, P> = {
  type: T;
  payload?: Partial<P>;
};

// Estado do contexto de arquivos
type FileContextState = {
  isLoading: boolean;
  file: File | null;
  fileList: File[];
  error: string | null;
};

// Definição do tipo para uma ação específica do contexto de arquivos
type FileAction = ReducerAction<FileActionType, Partial<FileContextState>>;

// Definição do tipo para a função dispatch do contexto de arquivos
type FileDispatch = ({ type, payload }: FileAction) => void;

// Definição do tipo para o contexto de arquivos
type FileContextType = {
  state: FileContextState;
  dispatch: FileDispatch;
};

// Definição do tipo para as props do FileProvider
type FileProviderProps = { children: ReactNode };

export type {
  FileContextState,
  FileAction,
  FileDispatch,
  FileContextType,
  FileProviderProps,
};
