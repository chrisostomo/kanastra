import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import * as Components from './components';
import FileUploadPage from './pages/FileUploadPage';
import FileListPage from './pages/FileListPage';
import { FileProvider } from './components/ui/file-provider'; // Certifique-se do caminho correto

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <FileProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<FileUploadPage />} />
          <Route path="/upload" element={<FileUploadPage />} />
          <Route path="/files" element={<FileListPage />} />
          <Route path="*" element={<Components.NoMatch />} />
        </Routes>
      </BrowserRouter>
    </FileProvider>
  </React.StrictMode>,
);
