import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCV, updateCV, shareCVByEmail } from '../services/api';

const CVDetail = () => {
  const [cv, setCv] = useState({});
  const [editMode, setEditMode] = useState(false);
  const { id } = useParams();

  useEffect(() => {
    const fetchCV = async () => {
      const data = await getCV(id);
      setCv(data);
    };
    fetchCV();
  }, [id]);

  const handleUpdate = async () => {
    await updateCV(id, cv);
    setEditMode(false);
  };

  const handleShare = async () => {
    await shareCVByEmail(id);
  };

  return (
    <div>
      <h1>CV Detail</h1>
      {editMode ? (
        <div>
          <input
            type="text"
            value={cv.name}
            onChange={(e) => setCv({ ...cv, name: e.target.value })}
          />
          <textarea
            value={cv.skills}
            onChange={(e) => setCv({ ...cv, skills: e.target.value })}
          />
          <textarea
            value={cv.experience}
            onChange={(e) => setCv({ ...cv, experience: e.target.value })}
          />
          <textarea
            value={cv.education}
            onChange={(e) => setCv({ ...cv, education: e.target.value })}
          />
          <button onClick={handleUpdate}>Save</button>
        </div>
      ) : (
        <div>
          <h3>Name: {cv.name}</h3>
          <p>Skills: {cv.skills}</p>
          <p>Experience: {cv.experience}</p>
          <p>Education: {cv.education}</p>
          <button onClick={() => setEditMode(true)}>Edit</button>
        </div>
      )}
      <button onClick={handleShare}>Share via Email</button>
    </div>
  );
};

export default CVDetail;
