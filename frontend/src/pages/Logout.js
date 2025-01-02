import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      const refreshToken = localStorage.getItem("refresh_token");
      const accessToken = localStorage.getItem("access_token");

      if (!refreshToken || !accessToken) {
        alert("You are not logged in.");
        navigate("/"); // Redirect to home if not logged in
        return;
      }

      try {
        await axios.post(
          "http://127.0.0.1:8000/apis/logout/",
          { refresh_token: refreshToken },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        // Clear tokens from localStorage
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        alert("Logout successful.");
        navigate("/"); // Redirect to home page
      } catch (err) {
        console.error("Logout error:", err.response?.data || err.message);
        alert("Error during logout. Please try again.");
        navigate("/"); // Redirect to home page even if logout fails
      }
    };

    handleLogout();
  }, [navigate]);

  return <p>Logging you out...</p>;
};

export default Logout;
