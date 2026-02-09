import axiosInstance from "./axiosInstance";

// Manager – get team leaves
export const getTeamLeaves = async () => {
  const response = await axiosInstance.get("/manager/leaves");
  return response.data;
};

// Manager – approve leave
export const approveLeaveByManager = async (leaveId) => {
  const response = await axiosInstance.put(`/manager/leave/${leaveId}/approve`);
  return response.data;
};

// Manager – reject leave
export const rejectLeaveByManager = async (leaveId) => {
  const response = await axiosInstance.put(`/manager/leave/${leaveId}/reject`);
  return response.data;
};
// Admin – get all pending leaves
export const getAllLeaves = async () => {
  const response = await axiosInstance.get("/admin/leaves");
  return response.data;
};

// Admin – approve leave
export const approveLeaveByAdmin = async (leaveId) => {
  const response = await axiosInstance.put(`/admin/leave/${leaveId}/approve`);
  return response.data;
};

// Admin – reject leave
export const rejectLeaveByAdmin = async (leaveId) => {
  const response = await axiosInstance.put(`/admin/leave/${leaveId}/reject`);
  return response.data;
};
