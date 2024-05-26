//import React from 'react';
import { render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect'; // Adicione esta linha
import FileListPage from '../pages/FileListPage';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

test('should fetch and display files',
  async () => {
    const files = [{filename: 'example.csv'}];
    mockedAxios.get.mockResolvedValueOnce({data: files});

    const {getByText} = render(<FileListPage/>);

    await waitFor(() => getByText('example.csv'));
    expect(getByText('example.csv')).toBeInTheDocument();
  });
