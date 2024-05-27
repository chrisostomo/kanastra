import { ReactNode } from "react";

export enum FileActionType {
  SET_LOADING = 'SET_LOADING',
  SET_FILE = 'SET_FILE',
  SET_FILE_LIST = 'SET_FILE_LIST',
  SET_ERROR = 'SET_ERROR',
}

export type ReducerAction<T, P> = {
  type: T;
  payload?: Partial<P>;
};

export type FileContextState = {
  isLoading: boolean;
  file: File | null;
  fileList: File[];
  error: string | null;
};

export type FileAction = ReducerAction<FileActionType, FileContextState>;

export type FileDispatch = ({ type, payload }: FileAction) => void;

export type FileContextType = {
  state: FileContextState;
  dispatch: FileDispatch;
  fetchFiles: () => Promise<void>;
  uploadFile: (formData: FormData) => Promise<void>;
};

export type FileProviderProps = { children: ReactNode };
