import API from "./axiosInstance";

// 🔹 Get all leaves
export const getAllLeaves = () => {
  return API.get("/admin/leaves");
};

// 🔹 Approve leave
export const approveLeaveByAdmin = (leaveId, remarks) => {
  return API.put(`/admin/leave/${leaveId}/approve`, remarks, {
    headers: { "Content-Type": "application/json" },
  });
};

export const rejectLeaveByAdmin = (leaveId, remarks) => {
  return API.put(`/admin/leave/${leaveId}/reject`, remarks, {
    headers: { "Content-Type": "application/json" },
  });
};