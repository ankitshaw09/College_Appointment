import React from 'react';
import { useState } from "react";
import { Link } from "react-router-dom";
// add css
import "./style.css";

const HomePage = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  return (
<div className="flex flex-col items-center justify-center h-screen bg-gray-100">

    <nav className="bg-white shadow-lg py-4 w-full fixed top-0">
      <div className="container mx-auto flex justify-between items-center px-8">
        <div className="text-xl font-bold text-blue-500">Logo</div>
        <ul className="flex items-center space-x-4">

          {/* Home */}
          <li>
            <Link to="/" className="text-lg text-gray-600 hover:text-blue-500">
              Home
            </Link>
          </li>

          {/* about */}
          <li>
            <Link
              to="/about"
              className="text-lg text-gray-600 hover:text-blue-500"
            >
              About
            </Link>
          </li>
          {/* contact */}
          <li>
            <Link
              to="/contact"
              className="text-lg text-gray-600 hover:text-blue-500"
            >
              Contact
            </Link>
          </li>

          {/* login */}
          <li className="dropdown">
            <button
              className="dropdown-button bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              Login 
            </button>
            {isDropdownOpen && (
              <ul className="dropdown-menu">
                <li>
                  <Link to="/login" className="dropdown-item">
                    Student Login
                  </Link>
                </li>
                <li>
                  <Link to="/ProfessorLogin" className="dropdown-item">
                    Professor Login
                  </Link>
                </li>
              </ul>
            )}
          </li>
          
          {/* register */}
          <li className="dropdown">
            <button
              className="dropdown-button bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              Register 
            </button>
            {isDropdownOpen && (
              <ul className="dropdown-menu">
                <li>
                  <Link to="/StudentRegister" className="dropdown-item">
                    Student Register
                  </Link>
                </li>
                <li>
                  <Link to="/ProfessorRegister" className="dropdown-item">
                    Professor Register
                  </Link>
                </li>
                
              </ul>
            )}
          </li>

        </ul>
      </div>
    </nav>


      <div className="bg-white rounded-lg shadow-lg p-8 w-1/2 mt-24">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to our Appointments System</h1>
        <p className="text-lg text-gray-600 mb-4">Manage your appointments with ease.</p>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Get Started</button>
      </div>
    </div>
  );
};

export default HomePage;
