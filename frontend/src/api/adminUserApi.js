import axios from "./axiosInstance";

export const getEmployees = () =>
  axios.get("/users/employees");

export const updateEmployeeManager = (employeeId, managerId) =>
  axios.put(`/users/employees/${employeeId}/manager?manager_id=${managerId}`);

export const deactivateEmployee = (employeeId) =>
  axios.put(`/users/employees/${employeeId}/deactivate`);