import { useAuth } from "../context/AuthContext";
import "./dashboard.css";

const Dashboard = () => {
  const { user } = useAuth();

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
          <p>Use the sidebar to manage leave, history, balance and approvals.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;