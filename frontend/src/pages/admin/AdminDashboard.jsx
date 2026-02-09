import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const AdminDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>

      <ul>
        <li>All Leave Approvals</li>
        <li>User Management</li>
      </ul>
<ul>
  <li onClick={() => navigate("/admin/approvals")}>
    All Leave Approvals
  </li>
  <li>User Management</li>
</ul>
    
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;
