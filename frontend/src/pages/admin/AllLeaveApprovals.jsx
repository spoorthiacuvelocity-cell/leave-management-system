import { useEffect, useState } from "react";
import {
  getAllLeaves,
  approveLeaveByAdmin,
  rejectLeaveByAdmin,
} from "../../api/adminApi";

import API from "../../api/axiosInstance";

import "../../styles/admin.css";

const AllLeaveApprovals = () => {

  const [leaves, setLeaves] = useState([]);
  const [month, setMonth] = useState("");
  const [employee, setEmployee] = useState("");
  const [leaveType, setLeaveType] = useState("");

  const fetchLeaves = async () => {
    try {
      const res = await getAllLeaves();
      setLeaves(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Failed to fetch leaves");
    }
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  // 🔹 Apply Filters
const fetchReports = async () => {
  try {

    const params = {};

    if (month) params.month = month;
    if (employee) params.employee_id = employee;
    if (leaveType) params.leave_type = leaveType;

    const res = await API.get("/admin/leave-reports", {
      params
    });

    setLeaves(Array.isArray(res.data) ? res.data : []);

  } catch (error) {
    console.error("Failed to fetch reports", error);
  }
};

  // 🔹 Export Filtered CSV
  const exportFiltered = async () => {
  try {

    const params = {};

    if (month) params.month = month;
    if (employee) params.employee_id = employee;
    if (leaveType) params.leave_type = leaveType;

    const response = await API.get("/admin/export-filtered", {
      params,
      responseType: "blob"
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = "filtered_leave_report.csv";
    a.click();

  } catch (error) {
    console.error("Export failed", error);
  }
};
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

      {/* 🔹 FILTER SECTION */}
      <div style={{ marginBottom: "20px" }}>

        <select onChange={(e) => setMonth(e.target.value)}>
          <option value="">Month</option>
          <option value="1">Jan</option>
          <option value="2">Feb</option>
          <option value="3">Mar</option>
          <option value="4">Apr</option>
          <option value="5">May</option>
          <option value="6">Jun</option>
          <option value="7">Jul</option>
          <option value="8">Aug</option>
          <option value="9">Sep</option>
          <option value="10">Oct</option>
          <option value="11">Nov</option>
          <option value="12">Dec</option>
        </select>

        <input
          type="number"
          placeholder="Employee ID"
          onChange={(e) => setEmployee(e.target.value)}
        />

        <select onChange={(e) => setLeaveType(e.target.value)}>
          <option value="">Leave Type</option>
          <option value="Sick">Sick</option>
          <option value="Casual">Casual</option>
          <option value="Annual">Annual</option>
        </select>

        <button onClick={fetchReports}>Apply Filters</button>

        <button onClick={exportFiltered}>
          Export Filtered CSV
        </button>
      </div>

      {leaves.length === 0 ? (
        <p>No leave requests found.</p>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Leave Type</th>
              <th>Dates</th>
              <th>Status</th>
              <th>Approved By</th>
              <th>Approved On</th>
              <th>Document</th>
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
                        minute: "2-digit",
                      })
                    : "—"}
                </td>

                <td>
  {leave.proof_document ? (
    <button
      onClick={() =>
        window.open(`http://localhost:8000/${leave.proof_document}`)
      }
    >
      Preview
    </button>
  ) : (
    "—"
  )}
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