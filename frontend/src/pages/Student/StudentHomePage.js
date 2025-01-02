import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
const StudentHomePage = () => {
  const studentName = localStorage.getItem("student_name");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [timeSlots, setTimeSlots] = useState([]); // State for time slots
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [appointments, setAppointments] = useState([]);

  // Fetch time slots from the backend
  useEffect(() => {
    const fetchTimeSlots = async () => {
      try {
        setLoading(true);
        const accessToken = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/apis/student/view_time_slots/",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`, // Add token to request
            },
          }
        );
        setTimeSlots(response.data.time_slots); // Set time slots
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to fetch time slots.");
      } finally {
        setLoading(false);
      }
    };
    fetchTimeSlots();

    const fetchAppointments = async () => {
      try {
        setLoading(true);
        const accessToken = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/apis/student/check_appointments/",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setAppointments(response.data.appointments || []);
      } catch (err) {
        setError(
          err.response?.data?.message || "Failed to fetch appointments."
        );
      } finally {
        setLoading(false);
      }
    };
    fetchAppointments();
  }, []);

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      {/* nav bar */}
      <nav className="bg-white shadow-lg py-4 w-full fixed top-0">
        <div className="container mx-auto flex justify-between items-center px-8">
          <div className="text-xl font-bold text-blue-500">Logo</div>
          <ul className="flex items-center space-x-4">
            {/* Home */}
            <li>
              <Link
                to="/StudentHomePage"
                className="text-lg text-gray-600 hover:text-blue-500"
              >
                Home
              </Link>
            </li>

            {/* login */}
            <li className="dropdown">
              <button
                className="dropdown-button bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                Appointment
              </button>
              {isDropdownOpen && (
                <ul className="dropdown-menu">
                  <li>
                    <Link to="/BookAppointmentPage" className="dropdown-item">
                      Booked Appointment
                    </Link>
                  </li>
                  <li>
                    <Link to="/CancelAppointmentPage" className="dropdown-item">
                      Cancel Appointment
                    </Link>
                  </li>
                </ul>
              )}
            </li>


            {/* logout */}
            <li>
              <Link
                to="/Logout"
                className="text-lg text-gray-600 hover:text-blue-500"
              >
                Logout
              </Link>
            </li>
          </ul>
        </div>
      </nav>

      {/* main content */}
      <div className="student-homepage-container">
        <div className="content-wrapper">
          <div className="  p-10 rounded-lg text-center shadow-md">
            <h2 className="text-3xl font-semibold ">
              Welcome, {studentName} !
            </h2>
          </div>
        </div>
      </div>

      {/* Time Slots Section */}
      <div className="TimeSlot-container">
        <div className="mt-10 p-5 bg-white rounded-lg shadow-md">
          <h3 className="text-2xl font-bold mb-4">Available Time Slots</h3>
          {loading && <p>Loading time slots...</p>}
          {error && <p className="text-red-500">{error}</p>}
          {!loading && !error && timeSlots.length === 0 && (
            <p>No time slots available.</p>
          )}
          <div className="overflow-x-auto">
            <table className="table-auto w-full border-collapse border border-gray-300">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border border-gray-300 px-4 py-2">
                    Time Slot ID
                  </th>
                  <th className="border border-gray-300 px-4 py-2">
                    Professor
                  </th>
                  <th className="border border-gray-300 px-4 py-2">
                    Department
                  </th>
                  <th className="border border-gray-300 px-4 py-2">Date</th>
                  <th className="border border-gray-300 px-4 py-2">Time</th>
                  <th className="border border-gray-300 px-4 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {timeSlots.map((slot) => (
                  <tr key={slot.time_slot_id}>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.time_slot_id}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.professor_name}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.professor_department}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.date}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.start_time} - {slot.end_time}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {slot.is_booked ? "Booked" : "Available"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {/* // </div> */}

      {/* Appointments Section */}
      <div className="Appointments-container">
      <div className="mt-10 p-5 bg-white rounded-lg shadow-md">
        <h3 className="text-2xl font-bold mb-4">Your Appointments</h3>
        {loading && <p>Loading appointments...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && appointments.length === 0 && (
          <p>You do not have any pending appointments.</p>
        )}
        {appointments.length > 0 && (
          <div className="overflow-x-auto">
            <table className="table-auto w-full border-collapse border border-gray-300">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border border-gray-300 px-4 py-2">
                    Appointment ID
                  </th>
                  <th className="border border-gray-300 px-4 py-2">
                    Professor
                  </th>
                  <th className="border border-gray-300 px-4 py-2">
                    Department
                  </th>
                  <th className="border border-gray-300 px-4 py-2">Date</th>
                  <th className="border border-gray-300 px-4 py-2">Time</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((appointment) => (
                  <tr key={appointment.appointment_id}>
                    <td className="border border-gray-300 px-4 py-2">
                      {appointment.appointment_id}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {appointment.professor_name}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {appointment.professor_department}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {appointment.date}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {appointment.start_time} - {appointment.end_time}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
    </div>

 );
};

export default StudentHomePage;
