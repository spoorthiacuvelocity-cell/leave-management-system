import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { loginUser } from "../api/authApi";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const data = await loginUser(email, password);

      const accessToken = data.access_token;

      // Create user object
      const userData = {
        name: data.name || email,
        role: data.role,
        gender: data.gender
      };

      // Store token and user
      login(accessToken, userData);

      // Role-based redirect
      if (userData.role === "ADMIN") {
        navigate("/admin/dashboard");
      } 
      else if (userData.role === "MANAGER") {
        navigate("/manager/dashboard");
      } 
      else {
        navigate("/employee/dashboard");
      }

    } catch (error) {
      console.error("Login error:", error.response?.data);
      alert(error.response?.data?.detail || "Invalid credentials");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin} autoComplete="off">
        <input
          type="email"
          placeholder="Enter email"
          autoComplete="new-email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br /><br />

        <input
          type="password"
          placeholder="Password"
          autoComplete="new-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br /><br />

        <button type="submit">Login</button>

        <p>
          Don’t have an account?
          <span
            style={{ color: "blue", cursor: "pointer" }}
            onClick={() => navigate("/register")}
          >
            Register
          </span>
        </p>
      </form>
    </div>
  );
};

export default Login;