import API from "./api";

export const getConfigurations = () =>
  API.get("/admin/configuration/");

export const addConfiguration = (data) =>
  API.post("/admin/configuration/", data);

export const updateConfiguration = (id, data) =>
  API.put(`/admin/configuration/${id}`, data);

export const deleteConfiguration = (id) =>
  API.delete(`/admin/configuration/${id}`);