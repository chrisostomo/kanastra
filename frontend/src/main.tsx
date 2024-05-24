import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { FileProvider } from './context/FileContext';
import FileUploader from './components/FileUploader';
import FileList from './components/FileList';
import NoMatch from './components/NoMatch';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <FileProvider>
        <Routes>
          <Route path="/" element={<FileUploader />} />
          <Route path="/list" element={<FileList />} />
          <Route path="*" element={<NoMatch />} />
        </Routes>
      </FileProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
