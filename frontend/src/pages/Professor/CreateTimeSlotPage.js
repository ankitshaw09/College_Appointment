import React, { useState } from "react";
import axios from "axios";

const CreateTimeSlotPage = () => {
  const [formData, setFormData] = useState({
    time_slot_id: "",
    date: "",
    start_time: "",
    end_time: "",
  });
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    try {
      const token = localStorage.getItem("access_token"); // Get the token from localStorage
      const response = await axios.post(
        "http://127.0.0.1:8000/apis/professor/timeslot/create/",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessage(response.data.message); // Set success message
      setFormData({
        time_slot_id: "",
        date: "",
        start_time: "",
        end_time: "",
      }); // Reset form
    } catch (err) {
      setError(
        err.response && err.response.data
          ? err.response.data.message || "Error creating time slot."
          : "Error creating time slot."
      );
    }
  };

  return (
    <div className="create-time-slot-container mt-10 p-5 bg-white rounded-lg shadow-md">
      <h3 className="text-2xl font-bold mb-4">Create a Time Slot</h3>
      {message && <p className="text-green-500 mb-4">{message}</p>}
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2">
            Time Slot ID
          </label>
          <input
            type="text"
            name="time_slot_id"
            value={formData.time_slot_id}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded-lg"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2">Date</label>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded-lg"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2">Start Time</label>
          <input
            type="time"
            name="start_time"
            value={formData.start_time}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded-lg"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2">End Time</label>
          <input
            type="time"
            name="end_time"
            value={formData.end_time}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded-lg"
            required
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
        >
          Create Time Slot
        </button>
      </form>
    </div>
  );
};

export default CreateTimeSlotPage;
