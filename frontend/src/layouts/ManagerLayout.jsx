import { Outlet, NavLink } from "react-router-dom";
import "./ManagerLayout.css";

const ManagerLayout = () => {

  return (
    <div className="manager-layout">

      <div className="manager-sidebar">

        <h2 className="manager-logo">Manager Panel</h2>

        <NavLink to="/manager/dashboard">
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

        <NavLink to="/manager/resignation">
          Resignation
        </NavLink>

        <NavLink to="/manager/approvals">
          Leave Approvals
        </NavLink>

      </div>

      <div className="manager-content">
        <Outlet />
      </div>

    </div>

  );

};

export default ManagerLayout;