import React, { useContext, useEffect } from 'react';
import { FileContext } from '../context/FileContext';
import axios from 'axios';

const FileList = () => {
  const context = useContext(FileContext);

  if (!context) {
    throw new Error('FileList must be used within a FileProvider');
  }

  const { state, dispatch } = context;

  useEffect(() => {
    const fetchFiles = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        const response = await axios.get('http://localhost:8080/files');
        dispatch({ type: 'SET_FILES', payload: response.data });
        dispatch({ type: 'SET_LOADING', payload: false });
      } catch (error) {
        dispatch({ type: 'SET_ERROR', payload: error.message });
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    fetchFiles();
  }, [dispatch]);

  return (
    <ul>
      {state.files.map((file, index) => (
        <li key={index}>{file.name}</li>
      ))}
    </ul>
  );
};

export default FileList;
