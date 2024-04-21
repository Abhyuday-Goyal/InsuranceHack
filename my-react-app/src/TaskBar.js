import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const TaskBar = () => {
  const navigate = useNavigate();

  return (
    <header className="task-bar">
      <div className="logo">YouSure?</div>
      <nav>
      <button onClick={() => navigate('/Home') } className="task-bar-button" style={{ fontSize: '1.1rem' }}>Home</button>
        
        <button onClick={() => navigate('/single-file')} className="task-bar-button" style={{ fontSize: '1.1rem' }}>Coverage Assesment</button>
        <button onClick={() => navigate('/search-notes') } className="task-bar-button" style={{ fontSize: '1.1rem' }}>Policy Query</button>
        {/* <Link to="/about" className="task-bar-link" style={{ fontSize: '1.1rem' }}>About Us</Link> */}
        
        <button onClick={() => navigate('/upload-policies') } className="task-bar-button" style={{ fontSize: '1.1rem' }}>Insurance Comparison</button>
        <Link to="/" className="task-bar-link" style={{ fontSize: '1.1rem' }}>Login</Link>
      </nav>
    </header>
  );
};

export default TaskBar;