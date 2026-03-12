import API from "./axiosInstance";

/* ================= LOGIN ================= */

export const loginUser = async (email, password) => {

const formData = new URLSearchParams();

formData.append("username", email);
formData.append("password", password);

const response = await API.post("/auth/login", formData, {
headers: {
"Content-Type": "application/x-www-form-urlencoded",
},
});

return response.data;

};

/* ================= REGISTER EMPLOYEE (ADMIN ONLY) ================= */

export const registerUser = async (data) => {

console.log("Sending register data:", data);

const token = localStorage.getItem("token");

const response = await API.post(
"/admin/register-employee",
{
name: data.name,
email: data.email,
password: data.password,
role: data.role.toUpperCase(),
gender: data.gender.toUpperCase(),
manager_id: data.manager_id
},
{
headers: {
Authorization: `Bearer ${token}`
}
}
);

return response.data;

};
