// SearchNotesPage.js
import React from 'react';
import './App.css';

const PolicyQuery = () => {
  return (
    <div className="search-notes-container">
      <div className="search-notes-content">
        <h1 className="search-notes-title fade-in">Query your Policy!</h1>
        <div className="search-notes-input-container fade-in">
          <input
            type="text"
            className="search-notes-input"
            placeholder="Type your question here"
          />
        </div>
      </div>
      <div className="backend-output-box fade-in"></div>
    </div>
  );
};

export default PolicyQuery;