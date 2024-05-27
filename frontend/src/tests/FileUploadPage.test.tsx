import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileProvider } from '@/components/ui/file-provider';
import FileUploadPage from '@/pages/FileUploadPage';
import { MESSAGES } from '@/constants/messages';

describe('FileUploadPage', () => {
  it('should render correctly', () => {
    render(
      <FileProvider>
        <FileUploadPage />
      </FileProvider>
    );
    expect(screen.getByText('Upload a File')).toBeInTheDocument();
    expect(screen.getByLabelText('fileInput')).toBeInTheDocument();
  });

  it('should handle file upload correctly', async () => {
    render(
      <FileProvider>
        <FileUploadPage />
      </FileProvider>
    );

    const file = new File(['content'], 'test-file.csv', { type: 'text/csv' });

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ id: 1, name: 'test-file.csv' })
      })
    ) as jest.Mock;

    const input = screen.getByLabelText('fileInput');
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(screen.getByText('Loading...')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());
  });

  it('should handle errors correctly', async () => {
    render(
      <FileProvider>
        <FileUploadPage />
      </FileProvider>
    );

    const file = new File(['content'], 'test-file.csv', { type: 'text/csv' });

    global.fetch = jest.fn(() =>
      Promise.reject(new Error(MESSAGES.ERROR.UPLOAD_FILE))
    ) as jest.Mock;

    const input = screen.getByLabelText('fileInput');
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(screen.getByText('Loading...')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText(`Error: ${MESSAGES.ERROR.UPLOAD_FILE}`)).toBeInTheDocument());
  });
});
