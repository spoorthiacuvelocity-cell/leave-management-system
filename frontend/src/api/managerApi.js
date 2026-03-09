import API from "./axiosInstance";

export const getPendingLeaves = () => {
  return API.get("/manager/team");
};

export const approveLeave = (id, remarks) => {
  return API.put(`/manager/leave/${id}/approve`, remarks);
};

export const rejectLeave = (id, remarks) => {
  return API.put(`/manager/leave/${id}/reject`, remarks);
};