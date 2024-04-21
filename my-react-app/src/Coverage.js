import React, { useState } from 'react';
import './Coverage.css';

const Coverage = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Uploading PDF file', file);

      const formData = new FormData();
      formData.append('pdf', file);

      try {
        await fetch('/single-file', {
          method: 'POST',
          body: JSON.stringify({ query: 'Coverage Analysis' }),
          headers: {
            'Content-Type': 'application/json'
          }
        });
        setUploadedFiles(prevFiles => [...prevFiles, file]);
      } catch (error) {
        console.error('Error uploading file:', error);
        // Handle error
      }

      event.target.value = null;
    }
  };

  const removeFile = (fileName) => {
    setUploadedFiles(uploadedFiles.filter(file => file.name !== fileName));
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
        <div className="backend-output-boxx fade-in"></div>
      </div>
    </div>
  );
};

export default Coverage;
