import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api/authApi";

const Register = () => {

  const navigate = useNavigate();

  const [managers, setManagers] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "EMPLOYEE",
    gender: "MALE",
    manager_id: ""
  });

  // Fetch managers
  useEffect(() => {

    fetch("http://localhost:8000/users/managers")
      .then((res) => res.json())
      .then((data) => {

        if (Array.isArray(data)) {
          setManagers(data);
        } else {
          setManagers([]);
        }

      })
      .catch((err) => {
        console.log("Error fetching managers:", err);
        setManagers([]);
      });

  }, []);

  const handleChange = (e) => {

    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value
    });

  };

  const handleRegister = async (e) => {

    e.preventDefault();

    try {

      const payload = {
        ...formData,
        manager_id:
          formData.role === "EMPLOYEE"
            ? Number(formData.manager_id)
            : null
      };

      console.log("Register payload:", payload);

      await registerUser(payload);

      alert("User registered successfully!");

      setFormData({
        name: "",
        email: "",
        password: "",
        role: "EMPLOYEE",
        gender: "MALE",
        manager_id: ""
      });

      navigate("/login");

    } catch (error) {

      console.log(error);

      if (error.response?.data?.detail) {

        const detail = error.response.data.detail;

        if (Array.isArray(detail)) {
          alert(detail.map((err) => err.msg).join(", "));
        } else {
          alert(detail);
        }

      } else {
        alert("Registration failed");
      }

    }

  };

  return (

    <div style={{ padding: "40px" }}>

      <h2>Register User</h2>

      <form
        onSubmit={handleRegister}
        autoComplete="off"
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "15px",
          maxWidth: "300px",
        }}
      >

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          autoComplete="new-email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          autoComplete="new-password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          required
        >
          <option value="MALE">Male</option>
          <option value="FEMALE">Female</option>
        </select>

        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          required
        >
          <option value="EMPLOYEE">Employee</option>
          <option value="MANAGER">Manager</option>
          <option value="ADMIN">Admin</option>
        </select>

        {/* Manager selection */}
        {formData.role === "EMPLOYEE" && (
          <select
            name="manager_id"
            value={formData.manager_id}
            onChange={handleChange}
            required
          >
            <option value="">Select Manager</option>

            {managers.map((manager) => (
              <option key={manager.id} value={manager.id}>
                {manager.name}
              </option>
            ))}

          </select>
        )}

        <button type="submit">
          Register
        </button>

      </form>

    </div>

  );

};

export default Register;