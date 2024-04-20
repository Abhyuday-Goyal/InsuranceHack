import React, { useState } from 'react';

const PdfUploadPage = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]); // Store uploaded files

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Uploading PDF file', file);
      // TODO: Send the file to the backend and store it
      uploadFileToBackend(file).then(() => {
        setUploadedFiles(prevFiles => [...prevFiles, file]);
      });
      event.target.value = null; // Reset the file input after handling upload
    }
  };

  const removeFile = (fileName) => {
    setUploadedFiles(uploadedFiles.filter(file => file.name !== fileName));
    // TODO: Also remove the file from the backend if needed
  };

  const handleButtonClick = () => {
    // Trigger file input click
    document.getElementById('pdf-upload').click();
  };

  const handleClearAll = () => {
    setUploadedFiles([]);
    // TODO: Also clear files from the backend if needed
  };

  // Simulate file upload to backend
  const uploadFileToBackend = async (file) => {
    // Replace this with actual file upload logic
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulating upload delay
    console.log('File uploaded to backend:', file.name);
  };

  return (
    <div className="file-upload-container">
      <h2 style={{ marginTop: '30px' }}>PDF File Upload</h2>
      <label htmlFor="pdf-upload" className="file-upload-button">
        Select File
      </label>
      <input
        type="file"
        id="pdf-upload"
        className="file-upload-input"
        accept=".pdf"
        onChange={handleUpload}
        style={{ display: 'none' }} // Hide the input element
      />
      <button onClick={handleButtonClick} className="file-upload-button">Upload PDF</button>
      <ul>
        {uploadedFiles.map((file, index) => (
          <li key={index}>
            {file.name}
            <button onClick={() => removeFile(file.name)} className="remove-file-button">
              Remove
            </button>
          </li>
        ))}
      </ul>
     
    </div>
  );
};

export default PdfUploadPage;
