// src/api/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Função para enviar arquivos
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${API_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

// Função para buscar arquivos
export const fetchFiles = async () => {
  return axios.get(`${API_URL}/files`);
};
