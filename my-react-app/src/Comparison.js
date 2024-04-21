import React, { useState } from 'react';
import './Comparison.css';

const Comparison = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [comparisonResult, setComparisonResult] = useState('');

  const handleUpload = async (event) => {
    // Code for handling file upload
  };

  const handleButtonClick = () => {
    document.getElementById('pdf-upload').click();
  };

  const compareFiles = async () => {
    try {
      const response = await fetch('/compare-policies', {
        method: 'GET'
      });
      const data = await response.json();
      setComparisonResult(data); // Update state with fetched data
    } catch (error) {
      console.error('Error comparing files:', error);
      // Handle error
    }
  }

  const handleClearAll = () => {
    setUploadedFiles([]);
  };

  return (
    <>
      <div className="file-upload-container">
        <h3>Compare Policies!</h3>
        <button onClick={handleButtonClick} className="select-file-button">UPLOAD PDF</button>
        <button onClick={handleButtonClick} className="upload-pdf-button">UPLOAD PDF</button>
        <button onClick={compareFiles} className="compare-button">COMPARE FILES</button>
        <input
          type="file"
          id="pdf-upload"
          className="file-upload-input"
          accept=".pdf"
          onChange={handleUpload}
          style={{ display: 'none' }} 
        />
      </div>

      <div className="backend-output-boxxx fade-in">{comparisonResult}</div>
    </>
  );
};

export default Comparison;
