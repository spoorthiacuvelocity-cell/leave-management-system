import API from "./axiosInstance";

/* ================= LOGIN ================= */
export const loginUser = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // FastAPI expects 'username'
  formData.append("password", password);

  const response = await API.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return response.data;
};


/* ================= REGISTER ================= */
export const registerUser = async (data) => {
  const response = await API.post("/auth/register", {
    name: data.name,
    email: data.email,
    password: data.password,
    role: data.role.toUpperCase(),
    gender: data.gender.toUpperCase(),
  });

  return response.data;
};