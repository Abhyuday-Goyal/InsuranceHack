import React, { useState } from 'react';
import './Comparison.css';

const Comparison = () => {
  const [comparisonResult, setComparisonResult] = useState('');
  const [pdf1, setPdf1] = useState(null);
  const [pdf2, setPdf2] = useState(null);

  const handleUpload1 = (event) => {
    const file = event.target.files[0];
    setPdf1(file);
  };

  const handleUpload2 = (event) => {
    const file = event.target.files[0];
    setPdf2(file);
  };

  const compareFiles = async () => {
    try {
      const formData = new FormData();
      formData.append('pdf1', pdf1);
      formData.append('pdf2', pdf2);

      const response = await fetch('http://127.0.0.1:5000/upload-policies', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      setComparisonResult(data.output);
    } catch (error) {
      console.error('Error comparing files:', error);
      // Handle error
    }
  };

  const handleButtonClick = () => {
    compareFiles();
  };

  return (
    <>
      <div className="file-upload-container">
        <div className="compare-container">
          <h2 style={{ marginRight: '140px' }}>Compare Policies!</h2>
          <div className="button-container-1">
            <label htmlFor="pdf-upload-1" className="file-upload-button-1">
              Select File 1
            </label>
            <input
              type="file"
              id="pdf-upload-1"
              className="file-upload-input"
              accept=".pdf"
              onChange={handleUpload1}
              style={{ display: 'none' }}
            />
          </div>
          <div className="button-container-2">
            <label htmlFor="pdf-upload-2" className="file-upload-button-2">
              Select File 2
            </label>
            <input
              type="file"
              id="pdf-upload-2"
              className="file-upload-input"
              accept=".pdf"
              onChange={handleUpload2}
              style={{ display: 'none' }}
            />
          </div>
          <div className="compare-button">
          <button onClick={handleButtonClick} className = "file-upload-button">Compare</button>
          </div>
        </div>
      </div>
      {comparisonResult && (
      <div className="fade-in max-w-[50vw] overflow-auto p-8 bg-[#444444] rounded-lg" style={{ whiteSpace: "pre-wrap" , fontSize: "6"}}>
      <p className='text-xl text-center'>{comparisonResult}</p>
  </div>
  )}
    </>
  );
};

export default Comparison;
