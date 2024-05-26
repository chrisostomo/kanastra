import React from 'react';
import { FileProvider } from '../components/ui/file';
import { FileUploader } from '../components/ui';

const FileUploadPage = () => {
  return (
    <FileProvider>
      <div>
        <h1>Upload CSV File</h1>
        <FileUploader />
      </div>
    </FileProvider>
  );
};

export default FileUploadPage;
