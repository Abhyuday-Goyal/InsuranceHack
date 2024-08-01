import React, { useState } from 'react';
import './Coverage.css';

const Coverage = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]); // Store uploaded files
  const [fileName, setFileName] = useState('');
  const [backendResponse, setBackendResponse] = useState('');

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    setFileName(event.target.files[0].name);
    const formData = new FormData();
    formData.append('pdf1', file);
    try {
      // Send the post request to your custom API
      const response = await fetch('http://127.0.0.1:5000/chat-search-data', {
        method: 'POST',
        body: formData,
      });
      // If successful, make a subsequent request to single-file
      const responseData = await response.json();
      console.log(responseData.output);
      setBackendResponse(responseData.output);
    } catch (error) {
      console.error('Error uploading file:', error);
      // Handle error state here (if needed)
    }
  };

  const removeFile = (fileName) => {
    setUploadedFiles(uploadedFiles.filter(file => file.name !== fileName));
    // TODO: Also remove the file from the backend if needed
  };

  return (
    <div className="file-upload-container">
      <div className="compare-container">
        <h2 style={{ marginRight: '140px' }}>Coverage Analysis</h2>
        <label htmlFor="pdf-upload" className="file-upload-button">
          Select File
        </label>
        <input
          type="file"
          id="pdf-upload"
          className="file-upload-input"
          accept=".pdf"
          onChange={handleUpload}
          style={{ display: 'none' }}
        />
        <ul className="gae">
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
      {backendResponse && (
  <div className="fade-in max-w-[50vw] overflow-auto p-8 bg-[#444444] rounded-lg" style={{ whiteSpace: "pre-wrap" , fontSize: "6"}}>
    <p className='text-xl text-center'>{backendResponse}</p>
  </div>
  )}
  </div>
  );
};

export default Coverage;
