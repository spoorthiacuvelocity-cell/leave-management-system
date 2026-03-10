import API from "./axiosInstance";

// 🔹 Get all leaves
export const getAllLeaves = () => {
  return API.get("/admin/leaves");
};

// 🔹 Approve leave
export const approveLeaveByAdmin = (leaveId, remarks) => {
  return API.put(`/admin/leave/${leaveId}/approve`, { remarks });
};

// 🔹 Reject leave
export const rejectLeaveByAdmin = (leaveId, remarks) => {
  return API.put(`/admin/leave/${leaveId}/reject`, { remarks });
};