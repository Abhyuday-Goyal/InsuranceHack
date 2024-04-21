import React, { useState } from 'react';
import './Form.css';

const Form = () => {
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    age: '',
    numberOfChildren: '',
    bmi: '',
    region: '',
    stateInitials: '', // Added new field
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <div className="form-container">
      <h2>User Details</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="gender">Gender:</label>
          <input
            type="text"
            id="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="age">Age:</label>
          <input
            type="number"
            id="age"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="numberOfChildren">Number of Children:</label>
          <input
            type="number"
            id="numberOfChildren"
            name="numberOfChildren"
            value={formData.numberOfChildren}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="bmi">BMI:</label>
          <input
            type="text"
            id="bmi"
            name="bmi"
            value={formData.bmi}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="region">Region:</label>
          <select
            id="region"
            name="region"
            value={formData.region}
            onChange={handleChange}
            required
          >
            <option value="">Select Region</option>
            <option value="NW">Northwest (NW)</option>
            <option value="NE">Northeast (NE)</option>
            <option value="SW">Southwest (SW)</option>
            <option value="SE">Southeast (SE)</option>
          </select>
        </div>
        {/* New form group for State (Initials) */}
        <div className="form-group">
          <label htmlFor="stateInitials">State (Initials):</label>
          <input
            type="text"
            id="stateInitials"
            name="stateInitials"
            value={formData.stateInitials}
            onChange={handleChange}
            required
          />
        </div>
        {/* Submit button */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Form;
