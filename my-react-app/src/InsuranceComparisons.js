import React from 'react';
import './InsuranceComparisons.css'; // Import CSS file for this component

const InsuranceComparisons = () => {
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    // Logic to handle file upload
    console.log('File uploaded:', file.name);
    // You can implement further logic here, such as uploading the file to a server
  };

  return (
    <div className="insurance-comparisons-container">
      <h2>Compare Files</h2>
      <div className="button-container">
        <label htmlFor="file-upload" className="upload-button">Upload File</label>
        <input id="file-upload" type="file" onChange={handleFileUpload} style={{ display: 'none' }} />
        <label htmlFor="file-upload" className="upload-button">Upload File</label>
        <input id="file-upload" type="file" onChange={handleFileUpload} style={{ display: 'none' }} />
      </div>
    </div>
  );
};

export default InsuranceComparisons;
