import { useEffect, useState } from "react";
import {
  getPendingResignations,
  approveResignation,
  rejectResignation
} from "../../api/resignationApi";

const AdminResignations = () => {
  const [resignations, setResignations] = useState([]);
  const [loading, setLoading] = useState(true);

  // 🔥 Fetch Pending Resignations
  const fetchResignations = async () => {
    try {
      const res = await getPendingResignations();
      setResignations(res.data);   // IMPORTANT
    } catch (error) {
      console.error("Failed to fetch resignations", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResignations();
  }, []);

  // 🔥 Approve
  const handleApprove = async (id) => {
    try {
      await approveResignation(id);
      fetchResignations(); // refresh list
    } catch (error) {
      console.error("Approve failed", error);
    }
  };

  // 🔥 Reject
  const handleReject = async (id) => {
    try {
      await rejectResignation(id);
      fetchResignations(); // refresh list
    } catch (error) {
      console.error("Reject failed", error);
    }
  };

  if (loading) return <p style={{ padding: "40px" }}>Loading...</p>;

  return (
    <div style={{ padding: "40px" }}>
      <h2>Pending Resignations</h2>

      {resignations.length === 0 ? (
        <p style={{ marginTop: "20px" }}>No pending resignations.</p>
      ) : (
        <table
          style={{
            marginTop: "20px",
            borderCollapse: "collapse",
            width: "100%"
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "#f5f5f5" }}>
              <th style={thStyle}>Employee Name</th>
              <th style={thStyle}>Email</th>
              <th style={thStyle}>Applied On</th>
              <th style={thStyle}>Action</th>
            </tr>
          </thead>
          <tbody>
            {resignations.map((emp) => (
              <tr key={emp.id}>
                <td style={tdStyle}>{emp.name}</td>
                <td style={tdStyle}>{emp.email}</td>
                <td style={tdStyle}>
                  {emp.resignation_date
                    ? new Date(emp.resignation_date).toLocaleDateString()
                    : "—"}
                </td>
                <td style={tdStyle}>
                  <button
                    style={approveBtn}
                    onClick={() => handleApprove(emp.id)}
                  >
                    Approve
                  </button>
                  <button
                    style={rejectBtn}
                    onClick={() => handleReject(emp.id)}
                  >
                    Reject
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const thStyle = {
  padding: "12px",
  textAlign: "left",
  borderBottom: "1px solid #ddd"
};

const tdStyle = {
  padding: "12px",
  borderBottom: "1px solid #eee"
};

const approveBtn = {
  backgroundColor: "#4CAF50",
  color: "white",
  border: "none",
  padding: "6px 12px",
  marginRight: "10px",
  cursor: "pointer",
  borderRadius: "4px"
};

const rejectBtn = {
  backgroundColor: "#EF5350",
  color: "white",
  border: "none",
  padding: "6px 12px",
  cursor: "pointer",
  borderRadius: "4px"
};

export default AdminResignations;