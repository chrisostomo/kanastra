import React, { useState } from 'react';
import { FileProvider } from '../components/ui/file-provider';
import { FileUploader } from '../components/ui/file-uploader';

const FileUploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  };

  return (
    <FileProvider>
      <div className="container mx-auto p-4 text-center">
        <h1 className="text-2xl mb-4">Upload a File</h1>
        <input
          id="fileInput"
          type="file"
          accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,text/csv"
          onChange={handleFileChange}
          className="mb-4"
        />
        <FileUploader file={file} />
      </div>
    </FileProvider>
  );
};

export default FileUploadPage;
