import { Routes, Route, Navigate } from "react-router-dom";

import Login from "../auth/Login";
import Register from "../auth/Register";
import NotAuthorized from "../pages/NotAuthorized";

import EmployeeDashboard from "../pages/employee/EmployeeDashboard";
import ApplyLeave from "../pages/employee/ApplyLeave";
import MyLeaves from "../pages/employee/MyLeaves";
import LeaveBalance from "../pages/employee/LeaveBalance";

import ManagerDashboard from "../pages/manager/ManagerDashboard";
import TeamLeaveApprovals from "../pages/manager/TeamLeaveApprovals";

import AdminDashboard from "../pages/admin/AdminDashboard";
import AllLeaveApprovals from "../pages/admin/AllLeaveApprovals";

import ProtectedRoute from "../auth/ProtectedRoute";
import RoleProtectedRoute from "../auth/RoleProtectedRoute";

const AppRoutes = () => {
  return (
    <Routes>

      {/* Default route */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* Public */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/not-authorized" element={<NotAuthorized />} />

      {/* Employee */}
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
        path="/employee/apply-leave"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["EMPLOYEE"]}>
              <ApplyLeave />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/employee/my-leaves"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["EMPLOYEE"]}>
              <MyLeaves />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/employee/leave-balance"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["EMPLOYEE"]}>
              <LeaveBalance />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      {/* Project Manager */}
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
        path="/manager/approvals"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["PROJECT_MANAGER"]}>
              <TeamLeaveApprovals />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

      {/* Admin */}
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

      <Route
        path="/admin/approvals"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={["ADMIN"]}>
              <AllLeaveApprovals />
            </RoleProtectedRoute>
          </ProtectedRoute>
        }
      />

    </Routes>
  );
};

export default AppRoutes;
