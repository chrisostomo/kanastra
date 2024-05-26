import React, { useEffect } from 'react';
import { FileProvider, useFileContext } from '../components/ui/file';
import { Table, TableHeader, TableBody, TableFooter, TableRow, TableHead, TableCell, TableCaption } from '../components/ui';

const FileList = () => {
  const { state, fetchFiles } = useFileContext();

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Filename</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {state.fileList.map((file, index) => (
          <TableRow key={index}>
            <TableCell>{file.filename}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell>Total: {state.fileList.length} files</TableCell>
        </TableRow>
      </TableFooter>
      <TableCaption>Uploaded Files</TableCaption>
    </Table>
  );
};

const FileListPage = () => {
  return (
    <FileProvider>
      <div>
        <h1>Uploaded Files</h1>
        <FileList />
      </div>
    </FileProvider>
  );
};

export default FileListPage;
