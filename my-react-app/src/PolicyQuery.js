// SearchNotesPage.js
import React ,{ useState } from 'react';
import './App.css';

const PolicyQuery = () => {
  const [query, setQuery] = useState('');
  const [backendOutput, setBackendOutput] = useState('');

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/single-file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'query': query }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      console.log(response)
      setQuery(''); // Clear the input field

      const data = await response.json();
      // setBackendOutput(data); // Assuming the response is a string or can be converted to one
      setBackendOutput(data.output); // Set the backend output to the response from Flask
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="search-notes-container">
      <div className="search-notes-content">
        <h1 className="search-notes-title fade-in">Chat with your policies!</h1>
        <div className="search-notes-input-container fade-in">
          <input
            type="text"
            className="search-notes-input mb-5 mt-2"
            placeholder="Type your question here"
            value={query}
            onChange={handleChange}
          />
          <button className="App-button mb-0" onClick={handleSubmit}>
            Submit
          </button>
        </div>
      </div>
        {backendOutput && <div className="fade-in max-w-[50vw] overflow-auto p-10 bg-[#444444] rounded-lg"><p className='text-xl text-center'>{backendOutput}</p></div>}
    </div>
  );
};

export default PolicyQuery;