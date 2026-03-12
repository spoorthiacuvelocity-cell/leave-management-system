import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./ManagerLayout.css";

const ManagerLayout = () => {

const { logout } = useAuth();
const navigate = useNavigate();

const handleLogout = () => {
logout();
navigate("/login");
};

return (

<div className="manager-layout">

  <div className="manager-sidebar">

    <h2 className="manager-logo">Manager Panel</h2>

    <NavLink to="/manager/dashboard" end>
      Dashboard
    </NavLink>

    <NavLink to="/manager/apply-leave">
      Apply Leave
    </NavLink>

    <NavLink to="/manager/leave-history">
      Leave History
    </NavLink>

    <NavLink to="/manager/leave-balance">
      Leave Balance
    </NavLink>

    <NavLink to="/manager/approvals">
      Leave Approvals
    </NavLink>

    <button className="logout-btn" onClick={handleLogout}>
      Logout
    </button>

  </div>

  <div className="manager-content">
    <Outlet />
  </div>

</div>

);

};

export default ManagerLayout;
