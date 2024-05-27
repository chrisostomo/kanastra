import React, { useEffect } from 'react';
import { useFileContext } from '../components/ui/file-provider';
import { cn } from '../lib/utils';
import {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableRow,
  TableHead,
  TableCell,
  TableCaption
} from '../components/ui/table';

const FileListPage: React.FC = () => {
  const { state, fetchFiles } = useFileContext();

  useEffect(() => {
    fetchFiles().catch(console.error);
  }, [fetchFiles]);

  return (
    <div className={cn("container mx-auto p-4 text-center")}>
      <h1 className={cn("text-2xl mb-4")}>Lista de Arquivos</h1>
      {state.isLoading ? (
        <p className={cn("text-gray-600")}>{MESSAGES.INFO.LOADING}</p>
      ) : (
        <Table className="table-auto">
          <TableHeader>
            <TableRow>
              <TableHead>Nome do Arquivo</TableHead>
              <TableHead>Data de Upload</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {state.fileList.map((file) => (
              <TableRow key={file.name}>
                <TableCell>{file.name}</TableCell>
                <TableCell>{new Date(file.uploadedAt).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
          {state.fileList.length === 0 && (
            <TableCaption>{MESSAGES.INFO.NO_FILES}</TableCaption>
          )}
          <TableFooter>
            <TableRow>
              <TableCell colSpan={2}>Total de arquivos: {state.fileList.length}</TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      )}
      {state.error && <p className={cn("text-red-600")}>{state.error}</p>}
    </div>
  );
};

export default React.memo(FileListPage);
