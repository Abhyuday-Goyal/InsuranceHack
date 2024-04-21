import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const TaskBar = () => {
  const navigate = useNavigate();

  return (
    <header className="task-bar">
      <div className="logo">AUTO</div>
      <nav>
        
        <Link to="/" className="task-bar-link" style={{ fontSize: '1.1rem' }}>Home</Link>
        <button onClick={() => navigate('/analyse')} className="task-bar-button" style={{ fontSize: '1.1rem' }}>Coverage Assesment</button>
        <button onClick={() => navigate('/search-notes') } className="task-bar-button" style={{ fontSize: '1.1rem' }}>Policy Query</button>
        {/* <Link to="/about" className="task-bar-link" style={{ fontSize: '1.1rem' }}>About Us</Link> */}
        
        <button onClick={() => navigate('/compare') } className="task-bar-button" style={{ fontSize: '1.1rem' }}>Insurance Comparison</button>
      </nav>
    </header>
  );
};

export default TaskBar;