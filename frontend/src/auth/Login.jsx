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

  const userData = {
    name: data.name || email,
    role: data.role,
    gender: data.gender
  };

  login(accessToken, userData);

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

<div style={styles.container}>

  <div style={styles.card}>

    <h2 style={styles.title}>Login</h2>

    <form onSubmit={handleLogin} autoComplete="off">

      <input
        type="email"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        style={styles.input}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        style={styles.input}
      />

      <div style={{ textAlign: "right", marginBottom: "15px" }}>
        <a href="/forgot-password" style={styles.forgot}>
          Forgot Password?
        </a>
      </div>

      <button type="submit" style={styles.button}>
        Login
      </button>

    </form>

  </div>

</div>


);

};

const styles = {

container: {
height: "100vh",
display: "flex",
justifyContent: "center",
alignItems: "center",
backgroundColor: "#f4f6f9"
},

card: {
width: "350px",
padding: "30px",
background: "white",
borderRadius: "8px",
boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
textAlign: "center"
},

title: {
marginBottom: "20px"
},

input: {
width: "100%",
padding: "10px",
marginBottom: "15px",
borderRadius: "4px",
border: "1px solid #ccc"
},

forgot: {
fontSize: "14px",
color: "#4A6FA5",
textDecoration: "none"
},

button: {
width: "100%",
padding: "10px",
backgroundColor: "#4A6FA5",
color: "white",
border: "none",
borderRadius: "4px",
cursor: "pointer"
}

};

export default Login;
