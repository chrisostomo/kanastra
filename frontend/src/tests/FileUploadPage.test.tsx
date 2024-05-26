//import React from 'react';
import '@testing-library/jest-dom/extend-expect';
import { render, fireEvent } from '@testing-library/react';
import FileUploadPage from '../pages/FileUploadPage';

test('should upload a file', () => {
  const { getByText, getByLabelText } = render(<FileUploadPage />);

  const file = new File(['dummy content'], 'example.csv', { type: 'text/csv' });
  const input = getByLabelText('Upload');
  fireEvent.change(input, { target: { files: [file] } });
  fireEvent.click(getByText('Upload'));

});
