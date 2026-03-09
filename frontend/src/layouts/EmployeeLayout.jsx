import { Outlet, Link } from "react-router-dom";
import "./EmployeeLayout.css";

const EmployeeLayout = () => {
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
          <Link to="/employee/resignation">Resignation</Link>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <Outlet />
      </div>

    </div>
  );
};

export default EmployeeLayout;