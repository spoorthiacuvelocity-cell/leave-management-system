import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./auth/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./auth/ProtectedRoute";
import EmployeeManagement from "./pages/admin/EmployeeManagement";
import AdminLayout from "./layouts/AdminLayout";
import EmployeeLayout from "./layouts/EmployeeLayout";
import ManagerLayout from "./layouts/ManagerLayout";

import Dashboard from "./pages/Dashboard";

import EmployeeLeave from "./pages/employee/EmployeeLeave";
import EmployeeHistory from "./pages/employee/EmployeeHistory";
import LeaveBalance from "./pages/employee/LeaveBalance";
import EmployeeResignation from "./pages/employee/EmployeeResignation";

import ManagerApprovals from "./pages/manager/ManagerApprovals";

import AllLeaveApprovals from "./pages/admin/AllLeaveApprovals";
import AdminResignations from "./pages/admin/AdminResignations";
import Configuration from "./pages/admin/Configuration";

import NotAuthorized from "./pages/NotAuthorized";

import { AuthProvider } from "./context/AuthContext";

const App = () => {
  return (
    <AuthProvider>

      <BrowserRouter>

        <Routes>

          {/* Public Routes */}
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/not-authorized" element={<NotAuthorized />} />

          {/* ================= EMPLOYEE ================= */}
          <Route
            path="/employee"
            element={
              <ProtectedRoute>
                <EmployeeLayout />
              </ProtectedRoute>
            }
          >

            <Route index element={<Navigate to="dashboard" />} />

            <Route path="dashboard" element={<Dashboard />} />
            <Route path="apply-leave" element={<EmployeeLeave />} />
            <Route path="leave-history" element={<EmployeeHistory />} />
            <Route path="leave-balance" element={<LeaveBalance />} />
            <Route path="resignation" element={<EmployeeResignation />} />

          </Route>

          {/* ================= MANAGER ================= */}
<Route
  path="/manager"
  element={
    <ProtectedRoute>
      <ManagerLayout />
    </ProtectedRoute>
  }
>

  <Route index element={<Navigate to="dashboard" />} />

  <Route path="dashboard" element={<Dashboard />} />

  <Route path="apply-leave" element={<EmployeeLeave />} />

  <Route path="leave-history" element={<EmployeeHistory />} />

  <Route path="leave-balance" element={<LeaveBalance />} />

  <Route path="resignation" element={<EmployeeResignation />} />

  <Route path="approvals" element={<ManagerApprovals />} />

</Route>

          {/* ================= ADMIN ================= */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminLayout />
              </ProtectedRoute>
            }
          >

            <Route index element={<Navigate to="dashboard" />} />
            <Route path="employees" element={<EmployeeManagement />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="leave-approvals" element={<AllLeaveApprovals />} />
            <Route path="resignations" element={<AdminResignations />} />
            <Route path="configuration" element={<Configuration />} />
            <Route path="register-employee" element={<Register />} />

          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/login" />} />

        </Routes>

      </BrowserRouter>

    </AuthProvider>
  );
};

export default App;