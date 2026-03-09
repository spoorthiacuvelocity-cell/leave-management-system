import API from "./axiosInstance";

// ================= APPLY LEAVE =================
export const applyLeave = (data) => {
  return API.post("/leave/apply", data, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};

// ================= GET MY LEAVES =================
export const getMyLeaves = () => {
  return API.get("/leave/my");
};

// ================= CANCEL LEAVE =================
export const cancelLeave = (leaveId) => {
  return API.put(`/leave/cancel/${leaveId}`);
};

// ================= GET LEAVE BALANCE =================
export const getLeaveBalance = () => {
  return API.get("/leave/balance");
};

// ================= GET LEAVE TYPES =================
export const getLeaveTypes = () => {
  return API.get("/leave/types");
};

// ================= APPLY RESIGNATION =================
export const applyResignation = async (data) => {
  const response = await API.post("/resignation/apply", data);
  return response.data;
};

// ================= MANAGER TEAM LEAVES =================
export const getManagerTeamLeaves = () => {
  return API.get("/manager/team");
};