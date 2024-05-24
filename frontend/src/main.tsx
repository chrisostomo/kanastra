import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import * as Components from './components/ui';
import { FileProvider } from './context/FileContext';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <FileProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Components.Layout />}>
            <Route index element={<Components.FileUploader />} />
            <Route path="table" element={<Components.FileTable />} />
            <Route path="*" element={<Components.NoMatch />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </FileProvider>
  </React.StrictMode>,
);
