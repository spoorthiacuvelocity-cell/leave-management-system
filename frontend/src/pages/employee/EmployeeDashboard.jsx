import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const EmployeeDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };
<ul>
  <li onClick={() => navigate("/employee/apply-leave")}>
    Apply Leave
  </li>
  <li onClick={() => navigate("/employee/my-leaves")}>
    My Leaves
  </li>
  <li onClick={() => navigate("/employee/leave-balance")}>
    Leave Balance
  </li>
</ul>


  return (
    <div>
      <h1>Employee Dashboard</h1>

      <ul>
        <li>Apply Leave</li>
        <li>My Leaves</li>
        <li>Leave Balance</li>
      </ul>

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default EmployeeDashboard;
