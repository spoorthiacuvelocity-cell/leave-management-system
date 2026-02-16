import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./auth/Login";
import ProtectedRoute from "./auth/ProtectedRoute";
import RoleProtectedRoute from "./auth/RoleProtectedRoute";

import EmployeeDashboard from "./pages/employee/EmployeeDashboard";
import ManagerDashboard from "./pages/manager/ManagerDashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";
import NotAuthorized from "./pages/NotAuthorized";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/not-authorized" element={<NotAuthorized />} />

      <Route
        path="/employee"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["EMPLOYEE"]}>
              <EmployeeDashboard />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/manager"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["PROJECT_MANAGER"]}>
              <ManagerDashboard />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["ADMIN"]}>
              <AdminDashboard />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default App;
