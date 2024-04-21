import React, { useState } from 'react';
import './Coverage.css';

const Coverage = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Uploading PDF file', file);
      uploadFileToBackend(file).then(() => {
        setUploadedFiles(prevFiles => [...prevFiles, file]);
      });
      event.target.value = null;
    }
  };

  const removeFile = (fileName) => {
    setUploadedFiles(uploadedFiles.filter(file => file.name !== fileName));
  };

  const handleButtonClick = () => {
    document.getElementById('pdf-upload').click();
  };

  const uploadFileToBackend = async (file) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('File uploaded to backend:', file.name);
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