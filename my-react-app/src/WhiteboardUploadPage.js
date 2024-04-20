// WhiteboardUploadPage.js
import React, { useState } from 'react';

const WhiteboardUploadPage = () => {
  const [pdfLink, setPdfLink] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    console.log('Uploading file for Whiteboard OCR', file);

    setIsProcessing(true);
    
    // TODO: Upload file to backend and handle response
  };

  return (
    <div className="file-upload-container" style={{ paddingLeft: '20px' }}>
      <h2 className="slide-in-left" style={{ marginTop: '30px' }}>Whiteboard Video Upload</h2>
      <label htmlFor="whiteboard-upload" className="file-upload-button">
        Select Video
      </label>
      <input
        type="file"
        id="whiteboard-upload"
        className="file-upload-input"
        accept="video/*"
        onChange={handleUpload}
      />
      {isProcessing && <div className="loader" style={{ margin: '20px auto' }}></div>}
      {pdfLink && !isProcessing && <a href={pdfLink} style={{ display: 'block', marginTop: '20px' }}>Download Processed PDF</a>}
    </div>
  );
};

export default WhiteboardUploadPage;