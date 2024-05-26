import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import * as Components from './components';
import FileUploadPage from './pages/FileUploadPage';
import FileListPage from './pages/FileListPage';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/upload" element={<FileUploadPage />} />
        <Route path="/files" element={<FileListPage />} />
        <Route path="*" element={<Components.NoMatch />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
