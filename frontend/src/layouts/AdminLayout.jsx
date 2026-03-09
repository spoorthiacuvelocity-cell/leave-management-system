import { Outlet, NavLink } from "react-router-dom";
import "./AdminLayout.css";

const AdminLayout = () => {

  return (
    <div className="admin-layout">

      <div className="admin-sidebar">

        <h2 className="admin-logo">Admin Panel</h2>

        <NavLink to="/admin/dashboard">
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

      </div>

      <div className="admin-content">
        <Outlet />
      </div>

    </div>
  );

};

export default AdminLayout;