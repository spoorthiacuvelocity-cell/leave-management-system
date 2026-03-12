import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";
import API from "../api/axiosInstance";
import "./dashboard.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {

  const { user } = useAuth();

  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    if (user?.role === "ADMIN") {
      fetchStats();
    }
  }, [user]);

  const fetchStats = async () => {
    try {

      const res = await API.get("/admin/leave-stats");

      const monthNames = [
        "", "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
      ];

      const labels = res.data.months.map(m => monthNames[m]);

      setChartData({
  labels: labels,
  datasets: [
  {
    label: "Leave Requests",
    data: res.data.counts,
    backgroundColor: "#5B6C8F",   // professional muted blue-gray
    borderColor: "#5B6C8F",
    borderWidth: 1,
    borderRadius: 6,              // rounded bars
    barThickness: 40              // thicker bars
  }
]
});
    } catch (error) {
      console.error("Failed to load chart data");
    }
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">

      <div className="dashboard-header">
        <h1>Leave Management System</h1>
        <p>Welcome, {user.name}</p>
      </div>

      <div className="dashboard-content">

        <div className="dashboard-card">
          <h3>Role</h3>
          <p>{user.role}</p>
        </div>

        <div className="dashboard-card">
          <h3>Status</h3>
          <p>You are logged in successfully.</p>
        </div>

        <div className="dashboard-card">
          <h3>Portal</h3>
          <p>Use the sidebar to manage leave requests and approvals.</p>
        </div>

        {/* Show chart only for ADMIN */}
        {user.role?.toUpperCase() === "ADMIN" && (
          <div className="dashboard-card">
            <h3>Leave Analytics</h3>
            <Bar data={chartData} />
          </div>
        )}

      </div>
    </div>
  );
};

export default Dashboard;