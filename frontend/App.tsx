import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import UserInput from './pages/UserInput';
import Result from './pages/Result';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/user" element={<UserInput />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </Router>
  );
}

export default App;