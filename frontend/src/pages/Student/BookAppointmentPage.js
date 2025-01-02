import React, { useState } from "react";
import axios from "axios";

const BookAppointmentPage = () => {
  const [timeSlotId, setTimeSlotId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [appointmentDetails, setAppointmentDetails] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccessMessage("");
    setAppointmentDetails(null);

    const token = localStorage.getItem("access_token"); // Retrieve the token

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/apis/student/book_appointment/",
        { time_slot_id: timeSlotId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setLoading(false);
      setSuccessMessage(response.data.message);
      setAppointmentDetails(response.data);
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.message || "An error occurred.");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <div className="p-6 bg-white shadow-md rounded-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Book an Appointment</h2>
        <form onSubmit={handleSubmit}>
          <label className="block mb-2 text-lg font-medium">
            Time Slot ID:
          </label>
          <input
            type="text"
            value={timeSlotId}
            onChange={(e) => setTimeSlotId(e.target.value)}
            className="w-full p-2 mb-4 border border-gray-300 rounded-lg"
            placeholder="Enter Time Slot ID"
            required
          />
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            disabled={loading}
          >
            {loading ? "Booking..." : "Book Appointment"}
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}
        {successMessage && (
          <div className="mt-6 bg-green-100 p-4 rounded-lg">
            <h3 className="text-lg font-semibold">{successMessage}</h3>
            {appointmentDetails && (
              <ul className="mt-4 text-gray-700">
                <li>
                  <strong>Appointment ID:</strong>{" "}
                  {appointmentDetails.appointment_id}
                </li>
                <li>
                  <strong>Time Slot ID:</strong>{" "}
                  {appointmentDetails.time_slot_id}
                </li>
                <li>
                  <strong>Student Name:</strong>{" "}
                  {appointmentDetails.student_name}
                </li>
                <li>
                  <strong>Professor Name:</strong>{" "}
                  {appointmentDetails.professor_name}
                </li>
                <li>
                  <strong>Department:</strong>{" "}
                  {appointmentDetails.professor_department}
                </li>
                <li>
                  <strong>Date:</strong> {appointmentDetails.date}
                </li>
                <li>
                  <strong>Time:</strong> {appointmentDetails.start_time} -{" "}
                  {appointmentDetails.end_time}
                </li>
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default BookAppointmentPage;
