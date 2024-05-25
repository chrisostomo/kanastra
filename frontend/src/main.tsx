import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { FileProvider } from './context/FileContext';
import Index from './pages/index';
import NoMatch from './pages/NoMatch/NoMatch.tsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <FileProvider>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="*" element={<NoMatch />} />
        </Routes>
      </FileProvider>
    </BrowserRouter>
  </React.StrictMode>
);
