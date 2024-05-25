import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { FileProvider } from './context/FileContext';
import IndexPage from './pages/Index';
import NoMatch from './pages/NoMatch';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <FileProvider>
        <Routes>
          <Route path="/" element={<IndexPage />} />
          <Route path="*" element={<NoMatch />} />
        </Routes>
      </FileProvider>
    </BrowserRouter>
  </React.StrictMode>
);
