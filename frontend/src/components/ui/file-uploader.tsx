import React, { useRef } from 'react';
import { useFileContext } from './file-provider';
import { cn } from '../../lib/utils';

export const FileUploader: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const { uploadFile } = useFileContext();

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      uploadFile(formData);
    }
  };

  return (
    <div className="flex flex-col items-center gap-6">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        className={cn("px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600")}
        onClick={handleUploadClick}
      >
        Upload File
      </button>
    </div>
  );
};
