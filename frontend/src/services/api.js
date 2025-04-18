import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

export const getCVs = async () => {
  try {
    const response = await axios.get(`${API_URL}cvs/`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the CVs!', error);
  }
};

export const createCV = async (cvData) => {
  try {
    const response = await axios.post(`${API_URL}cvs/`, cvData);
    return response.data;
  } catch (error) {
    console.error('There was an error creating the CV!', error);
  }
};

export const getCV = async (id) => {
  try {
    const response = await axios.get(`${API_URL}cvs/${id}/`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the CV details!', error);
  }
};

export const updateCV = async (id, cvData) => {
  try {
    const response = await axios.put(`${API_URL}cvs/${id}/`, cvData);
    return response.data;
  } catch (error) {
    console.error('There was an error updating the CV!', error);
  }
};

export const shareCVByEmail = async (id) => {
  try {
    const response = await axios.get(`${API_URL}share/email/${id}/`);
    return response.data;
  } catch (error) {
    console.error('There was an error sharing the CV by email!', error);
  }
};
