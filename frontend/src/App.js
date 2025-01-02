import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Navbar from './components/navbar';
import Logout from './pages/Logout';
import HomePage from './pages/HomePage';
import CancelAppointmentPage from './pages/CancelAppointmentPage';

import LoginPage from './pages/Student/StudentLoginPage';
import StudentHomePage from './pages/Student/StudentHomePage';
import StudentRegister from './pages/Student/StudentRegister';
import BookAppointmentPage from './pages/Student/BookAppointmentPage';

import ProfessorHomePage from './pages/Professor/ProfessorHomePage';
import ProfessorLogin from './pages/Professor/ProfessorLogin';
import ProfessorRegister from './pages/Professor/ProfessorRegister';
import CreateTimeSlotPage from './pages/Professor/CreateTimeSlotPage';


const App = () => {
  return (
    <Router>
      {/* <Navbar/> */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/CancelAppointmentPage" element={<CancelAppointmentPage />} />
        <Route path="/logout" element={<Logout />} />

        <Route path="/StudentHomePage" element={<StudentHomePage />} />
        <Route path="/StudentRegister" element={<StudentRegister />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/BookAppointmentPage" element={<BookAppointmentPage />} />

        <Route path="/ProfessorHomePage" element={<ProfessorHomePage />} />
        <Route path="/ProfessorLogin" element={<ProfessorLogin />} />
        <Route path="/ProfessorRegister" element={<ProfessorRegister />} />
        <Route path="/CreateTimeSlotPage" element={<CreateTimeSlotPage />} />
        
      </Routes>
    </Router>
  );
};

export default App;
