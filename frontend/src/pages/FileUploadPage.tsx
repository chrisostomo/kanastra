import React from 'react';
import { useFileContext } from '@/components/ui/file-provider';
import { FileUploader } from '@/components/ui/file-uploader';
import { cn } from '../lib/utils';
import {MESSAGES} from "@/constants/messages.ts";

const FileUploadPage: React.FC = () => {
  const { uploadFile, state } = useFileContext();

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      await uploadFile(formData);
    }
  };

  return (
    <div className={cn("container mx-auto p-4 text-center")}>
      <h1 className={cn("text-2xl mb-4")}>Upload a File</h1>
      <input
        id="fileInput"
        type="file"
        accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
        onChange={handleFileChange}
        className={cn("mb-4")}
      />
      <FileUploader />
      {state.isLoading && <p>{MESSAGES.INFO.LOADING}</p>}
      {state.error && <p className={cn("text-red-600")}>{state.error}</p>}
    </div>
  );
};

export default FileUploadPage;
