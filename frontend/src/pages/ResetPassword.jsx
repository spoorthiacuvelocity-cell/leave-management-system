import { useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

const ResetPassword = () => {

const { token } = useParams();
const navigate = useNavigate();

const [password, setPassword] = useState("");
const [confirmPassword, setConfirmPassword] = useState("");

const [showPassword, setShowPassword] = useState(false);
const [showConfirmPassword, setShowConfirmPassword] = useState(false);

const handleSubmit = async (e) => {
e.preventDefault();

if (password !== confirmPassword) {
  alert("Passwords do not match");
  return;
}

// Password strength validation
const strongPassword = /^(?=.*[A-Z])(?=.*[0-9]).{8,}$/;

if (!strongPassword.test(password)) {
  alert("Password must be at least 8 characters and include 1 uppercase letter and 1 number");
  return;
}

try {

  await axios.post("http://localhost:8000/auth/reset-password", {
    token: token,
    new_password: password
  });

  alert("Password reset successful");

  navigate("/login");

} catch (error) {

  if (error.response?.data?.detail) {
    alert(error.response.data.detail);
  } else {
    alert("Error resetting password");
  }

}


};

return (

<div style={styles.container}>

  <div style={styles.card}>

    <h2 style={styles.title}>Reset Password</h2>

    <form onSubmit={handleSubmit} style={styles.form}>

      <div style={styles.inputGroup}>
        <input
          type={showPassword ? "text" : "password"}
          placeholder="New Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          required
        />
        <span
          style={styles.eye}
          onClick={() => setShowPassword(!showPassword)}
        >
          👁
        </span>
      </div>

      <div style={styles.inputGroup}>
        <input
          type={showConfirmPassword ? "text" : "password"}
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          style={styles.input}
          required
        />
        <span
          style={styles.eye}
          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
        >
          👁
        </span>
      </div>

      <button type="submit" style={styles.button}>
        Reset Password
      </button>

    </form>

  </div>

</div>


);
};

const styles = {

container: {
display: "flex",
justifyContent: "center",
alignItems: "center",
height: "100vh",
background: "#f4f6f9",
padding: "20px"
},

card: {
width: "100%",
maxWidth: "420px",
background: "white",
padding: "35px",
borderRadius: "10px",
boxShadow: "0 8px 20px rgba(0,0,0,0.1)"
},

title: {
textAlign: "center",
marginBottom: "25px",
color: "#333"
},

form: {
display: "flex",
flexDirection: "column",
gap: "18px"
},

inputGroup: {
position: "relative"
},

input: {
width: "100%",
padding: "12px",
borderRadius: "6px",
border: "1px solid #ccc",
fontSize: "16px"
},

eye: {
position: "absolute",
right: "12px",
top: "50%",
transform: "translateY(-50%)",
cursor: "pointer",
fontSize: "18px"
},

button: {
padding: "12px",
background: "#1976d2",
color: "white",
border: "none",
borderRadius: "6px",
fontSize: "16px",
cursor: "pointer",
fontWeight: "bold"
}

};

export default ResetPassword;
