import { useState } from "react";
import axios from "axios";

const ForgotPassword = () => {

  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://localhost:8000/auth/forgot-password", {
        email: email
      });

      alert("Reset link sent to your email");

    } catch (error) {
      alert("Error sending reset link");
    }
  };

  return (

    <div style={styles.container}>

      <div style={styles.card}>

        <h2 style={styles.title}>Forgot Password</h2>

        <p style={styles.subtitle}>
          Enter your email to receive a reset link
        </p>

        <form onSubmit={handleSubmit} style={styles.form}>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
            required
          />

          <button type="submit" style={styles.button}>
            Send Reset Link
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
    maxWidth: "400px",
    background: "white",
    padding: "30px",
    borderRadius: "10px",
    boxShadow: "0 5px 20px rgba(0,0,0,0.1)"
  },

  title: {
    textAlign: "center",
    marginBottom: "10px"
  },

  subtitle: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#555"
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px"
  },

  input: {
    padding: "12px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    fontSize: "16px"
  },

  button: {
    padding: "12px",
    background: "#1976d2",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "16px",
    cursor: "pointer"
  }

};

export default ForgotPassword;