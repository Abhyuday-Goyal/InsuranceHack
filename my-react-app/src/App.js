// App.js
import React, { useState } from 'react';
import SearchNotesPage from './SearchNotesPage';
import { useNavigate } from 'react-router-dom';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WhiteboardUploadPage from './WhiteboardUploadPage';
import NotesUploadPage from './NotesUploadPage';
import PdfUploadPage from './PdfUploadPage';
import AboutUsPage from './AboutUsPage';
import TaskBar from './TaskBar';
import Compare from './Compare';

const App = () => {
  const [openDialog, setOpenDialog] = useState(false);

  const handleOptionClick = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    // Logic to handle file upload
    console.log('File uploaded:', file.name);
    // You can implement further logic here, such as uploading the file to a server
  };
  return (
    <Router>
      <div className="App">
        <TaskBar />
        <Routes>
          
       
          <Route path ="/compare" element = {<Compare></Compare>}/>
          <Route path="/search-notes" element={<SearchNotesPage />} />
          <Route path="/pdf-upload" element={<PdfUploadPage />} />
          <Route path="/about" element={<AboutUsPage />} />
        </Routes>
      </div>
    </Router>
  );
}



export default App;