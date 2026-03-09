import axiosInstance from "./axiosInstance";

export const getDashboardSummary = () =>
  axiosInstance.get("/dashboard/summary");