import React, { useState } from 'react';
import './Form.css';

const Form = () => {
  const [formData, setFormData] = useState({
    age: '',
    sex: '',
    bmi: '',
    children: '',
    smoker: '',
    region: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/add_person', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to add person');
      }

      const responseData = await response.json();
      console.log(responseData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="form-container">
      <h2>User Details</h2>
      <form onSubmit={handleSubmit}>
      <div className="form-group">
          <label htmlFor="username">UserName:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
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
          <label htmlFor="sex">Sex:</label>
          <input
            type="text"
            id="sex"
            name="sex"
            value={formData.sex}
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
          <label htmlFor="children">Children:</label>
          <input
            type="number"
            id="children"
            name="children"
            value={formData.children}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="smoker">Smoker:</label>
          <input
            type="text"
            id="smoker"
            name="smoker"
            value={formData.smoker}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="state">State:</label>
          <input
            type="text"
            id="state"
            name="state"
            value={formData.state}
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
            <option value="NW">northwest </option>
            <option value="NE">northeast </option>
            <option value="SW">southwest </option>
            <option value="SE">southeast </option>
          </select>
        </div>
        
        {/* Submit button */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Form;
