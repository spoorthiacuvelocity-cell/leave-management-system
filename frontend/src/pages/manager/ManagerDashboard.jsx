import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const ManagerDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div>
      <h1>Project Manager Dashboard</h1>

      <ul>
        <li>Team Leave Approvals (Priority)</li>
      </ul>
    <ul>
        <li onClick={() => navigate("/manager/approvals")}>
            Team Leave Approvals
         </li>
    </ul>

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default ManagerDashboard;
