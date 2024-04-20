import React from 'react';
import './AboutUsPage.css'; // Import CSS file for animations

function AboutUsPage() {
  return (
    <div className="about-us-page animation-fade-in" style={{ textAlign: 'left', padding: '20px' }}>
      <h1>About Us</h1>
      <p>
      As Computer Science majors at the University of Maryland, College Park, our passion for problem-solving drives us to innovate. 
      Our goal is to create a tangible solution with real-world applications, poised to make a meaningful impact in the lives of users. 
      Collaboratively, we've developed a cutting-edge web application with a focus on education. This project reflects our commitment 
      to leveraging technology for practical solutions and underscores our dedication to pushing the boundaries of what's possible in 
      the digital realm.
      </p>
      <h1>Team Members</h1>
      <ul>
        <li>Abhyuday Goyal ( abhyuday@umd.edu )</li>
        <li>Pranav Chandar Sridar ( pranav25@umd.edu )</li>
        <li>Swastik Agrawal ( swastik@umd.edu )</li>
        <li>Nishkal Hundia ( nhundia@umd.edu )</li>
      </ul>
    </div>
  );
}

export default AboutUsPage;