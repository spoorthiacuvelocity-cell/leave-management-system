import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const RoleProtectedRoute = ({ allowedRoles, children }) => {
  const { role } = useAuth();

  if (!allowedRoles.includes(role)) {
    return <Navigate to="/not-authorized" />;
  }

  return children;
};

export default RoleProtectedRoute;
