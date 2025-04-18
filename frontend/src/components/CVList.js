import React, { useEffect, useState } from 'react';
import { getCVs } from '../services/api';
import { Link } from 'react-router-dom';

const CVList = () => {
  const [cvs, setCvs] = useState([]);

  useEffect(() => {
    const fetchCVs = async () => {
      const data = await getCVs();
      setCvs(data);
    };
    fetchCVs();
  }, []);

  return (
    <div>
      <h1>CV List</h1>
      <Link to="/create">Create a new CV</Link>
      <ul>
        {cvs.map((cv) => (
          <li key={cv.id}>
            <Link to={`/cvs/${cv.id}`}>{cv.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CVList;
