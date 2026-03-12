import API from "./axiosInstance";

// ================= APPLY LEAVE =================
export const applyLeave = async (data) => {
const response = await API.post("/leave/apply", data, {
headers: {
"Content-Type": "multipart/form-data"
}
});

return response.data;
};

// ================= GET MY LEAVES =================
export const getMyLeaves = async () => {
const response = await API.get("/leave/my");
return response.data;
};

// ================= CANCEL LEAVE =================
export const cancelLeave = async (leaveId) => {
const response = await API.put(`/leave/cancel/${leaveId}`);
return response.data;
};

// ================= GET LEAVE BALANCE =================
export const getLeaveBalance = async () => {
const response = await API.get("/leave/balance");
return response.data;
};

// ================= GET LEAVE TYPES =================
export const getLeaveTypes = async () => {
const response = await API.get("/leave/types");
return response.data;
};

// ================= APPLY RESIGNATION =================
export const applyResignation = async (data) => {
const response = await API.post("/resignation/apply", data);
return response.data;
};

// ================= MANAGER TEAM LEAVES =================
export const getManagerTeamLeaves = async () => {
const response = await API.get("/manager/team");
return response.data;
};
