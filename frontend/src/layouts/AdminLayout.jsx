import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./AdminLayout.css";

const AdminLayout = () => {

const auth = useAuth();
const navigate = useNavigate();

const handleLogout = () => {
auth.logout();
navigate("/login");
};

return (

<div className="admin-layout">

  <div className="admin-sidebar">

    <h2 className="admin-logo">Admin Panel</h2>

    <NavLink to="/admin/dashboard" end>
      Dashboard
    </NavLink>

    <NavLink to="/admin/leave-approvals">
      Leave Approvals
    </NavLink>

    <NavLink to="/admin/employees">
      Employees
    </NavLink>

    <NavLink to="/admin/resignations">
      Resignations
    </NavLink>

    <NavLink to="/admin/register-employee">
      Register Employee
    </NavLink>

    <NavLink to="/admin/configuration">
      Configuration
    </NavLink>

    <button className="logout-btn" onClick={handleLogout}>
      Logout
    </button>

  </div>

  <div className="admin-content">
    <Outlet />
  </div>

</div>


);

};

export default AdminLayout;
