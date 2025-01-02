import React, { useState } from "react";
import axios from "axios";

const CancelAppointmentPage = () => {
  const [appointmentId, setAppointmentId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccessMessage("");

    const token = localStorage.getItem("access_token"); // Retrieve the token

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/apis/professor/cancel_appointment/",
        { appointment_id: appointmentId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setLoading(false);
      setSuccessMessage(response.data.message);
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.message || "An error occurred.");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <div className="p-6 bg-white shadow-md rounded-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Cancel an Appointment</h2>
        <form onSubmit={handleSubmit}>
          <label className="block mb-2 text-lg font-medium">
            Appointment ID:
          </label>
          <input
            type="text"
            value={appointmentId}
            onChange={(e) => setAppointmentId(e.target.value)}
            className="w-full p-2 mb-4 border border-gray-300 rounded-lg"
            placeholder="Enter Appointment ID"
            required
          />
          <button
            type="submit"
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            disabled={loading}
          >
            {loading ? "Cancelling..." : "Cancel Appointment"}
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}
        {successMessage && (
          <p className="text-green-500 mt-4">{successMessage}</p>
        )}
      </div>
    </div>
  );
};

export default CancelAppointmentPage;
