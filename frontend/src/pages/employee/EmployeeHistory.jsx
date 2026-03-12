import { useEffect, useState } from "react";
import { getMyLeaves, cancelLeave } from "../../api/leaveApi";
import "../../styles/configuration.css";

const EmployeeHistory = () => {

  const [leaveRequests, setLeaveRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("ALL");
  const [resignationApproved, setResignationApproved] = useState(false);

  const fetchLeaves = async () => {

    try {

      const response = await getMyLeaves();

      if (Array.isArray(response)) {
        setLeaveRequests(response);
      } else {
        setLeaveRequests([]);
      }

    } catch (error) {

      if (error.response?.status === 403) {
        setResignationApproved(true);
      } else {
        console.log("Error fetching leaves:", error);
      }

    } finally {
      setLoading(false);
    }

  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  const handleCancel = async (id) => {

    if (resignationApproved) return;

    try {
      await cancelLeave(id);
      fetchLeaves();
    } catch (error) {
      alert(error.response?.data?.detail || "Cancel failed");
    }

  };

  const filteredLeaves =
    filter === "ALL"
      ? leaveRequests
      : leaveRequests.filter(
          (leave) => leave.status?.toUpperCase() === filter
        );

  return (

    <div className="card">

      <h2>My Leave History</h2>

      {resignationApproved && (
        <div
          style={{
            background: "#fff3cd",
            padding: "12px",
            borderRadius: "6px",
            marginBottom: "15px"
          }}
        >
          ⚠ Your resignation has been approved. Leave actions are disabled.
        </div>
      )}

      <div style={{ marginBottom: "15px" }}>
        <label style={{ marginRight: "10px" }}>Filter:</label>

        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="ALL">All</option>
          <option value="PENDING">Pending</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : filteredLeaves.length === 0 ? (
        <p>No leave records found.</p>
      ) : (

        <table className="leave-table">

          <thead>
            <tr>
              <th>Type</th>
              <th>From</th>
              <th>To</th>
              <th>Days</th>
              <th>Status</th>
              <th>Remarks</th>
              <th>Applied On</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {filteredLeaves.map((leave) => (

              <tr key={leave.id}>

                <td>{leave.leave_type}</td>
                <td>{leave.start_date}</td>
                <td>{leave.end_date}</td>
                <td>{leave.number_of_days}</td>

                <td>
                  <span className={`status-badge ${leave.status?.toLowerCase()}`}>
                    {leave.status}
                  </span>
                </td>

                <td>{leave.reason || "-"}</td>
                <td>{leave.created_at || "-"}</td>

                <td>
                  {leave.status?.toUpperCase() === "PENDING" && !resignationApproved && (
                    <button
                      className="danger-btn"
                      onClick={() => handleCancel(leave.id)}
                    >
                      Cancel
                    </button>
                  )}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>

  );

};

export default EmployeeHistory;