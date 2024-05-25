import React from 'react';
import FileList from './components/FileList';
import FileUploader from './components/FileUploader';

const App = () => {
  return (
    <div className="App">
      <FileList />
      <FileUploader />
    </div>
  );
};

export default App;
