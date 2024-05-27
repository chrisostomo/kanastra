import React from 'react';

type FileUploaderProps = {
  file: File | null;
};

const FileUploader: React.FC<FileUploaderProps> = ({ file }) => {
  const handleUploadClick = () => {
    if (file) {
      // Lógica de upload de arquivo aqui
      console.log('Uploading file:', file);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {file && (
        <section>
          <p className="pb-6">File details:</p>
          <ul>
            <li>Name: {file.name}</li>
            <li>Type: {file.type}</li>
            <li>Size: {file.size} bytes</li>
          </ul>
        </section>
      )}

      {file && (
        <button
          className="rounded-lg bg-green-800 text-white px-4 py-2 border-none font-semibold"
          onClick={handleUploadClick}
        >
          Upload the file
        </button>
      )}
    </div>
  );
};

export { FileUploader };
