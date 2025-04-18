import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CVList from './components/CVList';
import CVForm from './components/CVForm';
import CVDetail from './components/CVDetail';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={<CVList />}
        />
        <Route
          path="/create"
          element={<CVForm />}
        />
        <Route
          path="/cvs/:id"
          element={<CVDetail />}
        />
      </Routes>
    </Router>
  );
};

export default App;
