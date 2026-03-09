import { useEffect, useState } from "react";
import {
  getAllLeaves,
  approveLeaveByAdmin,
  rejectLeaveByAdmin,
} from "../../api/adminApi";

import "../../styles/admin.css";

const AllLeaveApprovals = () => {
  const [leaves, setLeaves] = useState([]);

  const fetchLeaves = async () => {
    try {
      const res = await getAllLeaves();
      setLeaves(res.data || []);
    } catch (error) {
      console.error("Failed to fetch leaves");
    }
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  const handleApprove = async (id) => {
    const remarks = prompt("Enter approval remarks:");
    await approveLeaveByAdmin(id, remarks);
    fetchLeaves();
  };

  const handleReject = async (id) => {
    const remarks = prompt("Enter rejection remarks:");
    await rejectLeaveByAdmin(id, remarks);
    fetchLeaves();
  };

  return (
    <div className="admin-card">
      <h2>📋 All Leave Requests</h2>

      {leaves.length === 0 ? (
        <p>No leave requests found.</p>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Type</th>
              <th>Dates</th>
              <th>Status</th>
              <th>Approved By</th>
              <th>Approved On</th>
              <th>Remarks</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {leaves.map((leave) => (
              <tr key={leave.id}>
                <td>{leave.user_id}</td>
                <td>{leave.leave_type}</td>
                <td>
                  {leave.start_date} → {leave.end_date}
                </td>
                <td>
                  <span className={`status-badge ${leave.status.toLowerCase()}`}>
                    {leave.status}
                  </span>
                </td>
                <td>{leave.approved_by_role || "—"}</td>
               <td>
  {leave.approved_on
    ? new Date(leave.approved_on).toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      })
    : "—"}
</td>
                <td>{leave.remarks || "—"}</td>

                <td>
                  {leave.status === "Pending" && (
                    <>
                      <button onClick={() => handleApprove(leave.id)}>
                        Approve
                      </button>
                      <button onClick={() => handleReject(leave.id)}>
                        Reject
                      </button>
                    </>
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

export default AllLeaveApprovals;