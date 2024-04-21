import React, { useState } from 'react';
import './Comparison.css';
const clearDatabase = async () => {
  try {
    await fetch('/clear_database', {
      method: 'GET'
    });
    console.log('Database cleared!');
  } catch (error) {
    console.error('Error clearing database:', error);
    // Handle error
  }
};

const Comparison = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Uploading PDF file', file);
  
      const formData = new FormData();
      formData.append('pdf1', file);
  
      try {
        await fetch('/upload-policies', {
          method: 'POST',
          body: formData,
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

  const handleButtonClick = () => {
    document.getElementById('pdf-upload').click();
  };

  const handleClearAll = () => {
    setUploadedFiles([]);
  };

  const uploadFileToBackend = async (file) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('File uploaded to backend:', file.name);
  };

  return (
    <>
    <div className="file-upload-container">
      <h3>Compare Policies!</h3>
      <button onClick={handleButtonClick} className="select-file-button">UPLOAD PDF</button>
      <button onClick={handleButtonClick} className="upload-pdf-button">UPLOAD PDF</button>
      <input
        type="file"
        id="pdf-upload"
        className="file-upload-input"
        accept=".pdf"
        onChange={handleUpload}
        style={{ display: 'none' }} 
      />
      
      {/* Directly apply styles without using a div */}
      
    </div>
    <div className="backend-output-boxxx fade-in"></div>
    </>
    
  );
};

export default Comparison;
