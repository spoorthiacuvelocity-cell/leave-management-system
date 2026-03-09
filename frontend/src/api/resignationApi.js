import API from "./api";

// 🔹 Employee applies resignation
export const applyResignation = (data) =>
  API.post("/resignation/apply", data);

// 🔹 Admin gets pending resignations
export const getPendingResignations = () =>
  API.get("/resignation/pending");

// 🔹 Admin approves resignation
export const approveResignation = (userId) =>
  API.put(`/resignation/approve/${userId}`);

// 🔹 Admin rejects resignation
export const rejectResignation = (userId) =>
  API.put(`/resignation/reject/${userId}`);
export const getMyResignation = () =>
  API.get("/resignation/my");