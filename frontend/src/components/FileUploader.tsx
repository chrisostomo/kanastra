import React, { useState, useContext } from 'react';
import { FileContext } from '../context/FileContext';
import axios from 'axios';

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const context = useContext(FileContext);

  if (!context) {
    throw new Error('FileUploader must be used within a FileProvider');
  }

  const { dispatch } = context;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8000/upload', formData);
      dispatch({ type: 'ADD_FILE', payload: response.data });
      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept=".csv, application/vnd.ms-excel" />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUploader;
