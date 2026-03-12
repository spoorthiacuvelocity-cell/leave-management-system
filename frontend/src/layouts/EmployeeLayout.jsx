import { Outlet, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./EmployeeLayout.css";

const EmployeeLayout = () => {

const auth = useAuth();
const navigate = useNavigate();

const handleLogout = () => {
auth.logout();
navigate("/login");
};

return (


<div className="layout">

  {/* Sidebar */}
  <div className="sidebar">

    <h2 className="logo">Employee</h2>

    <nav>
      <Link to="/employee/dashboard">Dashboard</Link>
      <Link to="/employee/apply-leave">Apply Leave</Link>
      <Link to="/employee/leave-history">Leave History</Link>
      <Link to="/employee/leave-balance">Leave Balance</Link>
    </nav>

    <button className="logout-btn" onClick={handleLogout}>
      Logout
    </button>

  </div>

  {/* Main Content */}
  <div className="main-content">
    <Outlet />
  </div>

</div>


);

};

export default EmployeeLayout;
