import { useEffect, useState } from "react";
import axios from "axios";

const AdminResignations = () => {

const [employees, setEmployees] = useState([]);
const [selectedUser, setSelectedUser] = useState("");
const [noticeDays, setNoticeDays] = useState("");
const [reason, setReason] = useState("");

const token = localStorage.getItem("token");

useEffect(() => {
fetchEmployees();
}, []);

const fetchEmployees = async () => {
try {
const res = await axios.get(
"http://localhost:8000/admin/employees",
{
headers: {
Authorization: `Bearer ${token}`
}
}
);

  setEmployees(res.data);

} catch (error) {
  console.error(error);
}


};

const handleSubmit = async (e) => {

e.preventDefault();

try {

  const res = await axios.post(
    "http://localhost:8000/admin/mark-resigned",
    {
      user_id: parseInt(selectedUser),
      notice_days: parseInt(noticeDays),
      reason: reason
    },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  alert(res.data.message);

  setSelectedUser("");
  setNoticeDays("");
  setReason("");

} catch (error) {

  alert(error.response?.data?.detail || "Something went wrong");

}


};

return (

<div style={styles.container}>

  <div style={styles.card}>

    <h2 style={styles.title}>
      Resignation Management
    </h2>

    <form onSubmit={handleSubmit}>

      <div style={styles.field}>
        <label>Select Employee / Manager</label>

        <select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
          style={styles.input}
          required
        >

          <option value="">Select Employee</option>

          {employees.map((emp) => (
            <option key={emp.id} value={emp.id}>
              {emp.name} ({emp.role})
            </option>
          ))}

        </select>
      </div>

      <div style={styles.field}>
        <label>Notice Period (Days)</label>

        <input
          type="number"
          value={noticeDays}
          onChange={(e) => setNoticeDays(e.target.value)}
          style={styles.input}
          required
        />
      </div>

      <div style={styles.field}>
        <label>Reason</label>

        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          style={styles.textarea}
        />
      </div>

      <button type="submit" style={styles.button}>
        Mark Resigned
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
height: "80vh",
background: "#f4f6f9"
},

card: {
background: "white",
padding: "30px",
borderRadius: "10px",
width: "420px",
boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
},

title: {
textAlign: "center",
fontWeight: "600",
marginBottom: "25px",
color: "#1e293b"
},

field: {
display: "flex",
flexDirection: "column",
marginBottom: "15px"
},

input: {
padding: "8px",
borderRadius: "6px",
border: "1px solid #ccc",
marginTop: "5px"
},

textarea: {
padding: "8px",
borderRadius: "6px",
border: "1px solid #ccc",
marginTop: "5px"
},

button: {
width: "100%",
padding: "10px",
background: "#2563eb",
color: "white",
border: "none",
borderRadius: "6px",
cursor: "pointer",
fontWeight: "bold"
}

};

export default AdminResignations;
