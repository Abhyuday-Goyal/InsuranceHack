// App.js
import React, { useState } from 'react';
import PolicyQuery from './PolicyQuery';
import { useNavigate } from 'react-router-dom';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Comparison from './Comparison';

import TaskBar from './TaskBar';
import Coverage from './Coverage';
import Form from './Form'

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
          
          <Route path ="/" element = {<Form></Form>}/>
          <Route path ="/upload-policies" element = {<Comparison></Comparison>}/>

          <Route path="/search-notes" element={<PolicyQuery />} />
         
          <Route path="/single-file" element=   {<Coverage/>}/>
          
        
        </Routes>
      </div>
    </Router>
  );
}
export default App;