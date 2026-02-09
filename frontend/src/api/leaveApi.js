import axiosInstance from "./axiosInstance";

export const applyLeave = async (leaveData) => {
  const response = await axiosInstance.post(
    "/leave/apply",
    leaveData
  );
  return response.data;
};
