import React, { useState } from 'react';
import { createCV } from '../services/api';
import { useNavigate } from 'react-router-dom';

const CVForm = () => {
  const [name, setName] = useState('');
  const [skills, setSkills] = useState('');
  const [experience, setExperience] = useState('');
  const [education, setEducation] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newCV = { name, skills, experience, education };
    await createCV(newCV);
    navigate('/');
  };

  return (
    <div>
      <h1>Create CV</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Skills"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
        <input
          type="text"
          placeholder="Experience"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
        />
        <input
          type="text"
          placeholder="Education"
          value={education}
          onChange={(e) => setEducation(e.target.value)}
        />
        <button type="submit">Create</button>
      </form>
    </div>
  );
};

export default CVForm;
