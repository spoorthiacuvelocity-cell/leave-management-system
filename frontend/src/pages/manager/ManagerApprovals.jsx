import { useEffect, useState } from "react";
import {
  getPendingLeaves,
  approveLeave,
  rejectLeave
} from "../../api/managerApi";
import "../../styles/manager.css";

const ManagerApprovals = () => {

  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedLeave, setSelectedLeave] = useState(null);
  const [actionType, setActionType] = useState(null);

  // 🔹 Fetch manager team leave requests
  const fetchLeaves = async () => {

    try {

      const res = await getPendingLeaves();

      if (Array.isArray(res.data)) {
        setLeaves(res.data);
      } else {
        setLeaves([]);
      }

    } catch (error) {

      console.log("Error fetching leaves:", error.response?.data);
      setLeaves([]);

    } finally {
      setLoading(false);
    }

  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  // 🔹 Approve / Reject confirmation
  const confirmAction = async () => {

    if (!selectedLeave) return;

    try {

      if (actionType === "approve") {
        await approveLeave(selectedLeave.id);
      } else {
        await rejectLeave(selectedLeave.id);
      }

      await fetchLeaves();

    } catch (error) {

      alert(error.response?.data?.detail || "Action failed");

    } finally {

      setSelectedLeave(null);
      setActionType(null);

    }

  };

  // 🔹 Search filter
  const filteredLeaves = leaves.filter((leave) => {

    if (!search) return true;

    return (
      leave.employee_name?.toLowerCase().includes(search.toLowerCase()) ||
      leave.leave_type?.toLowerCase().includes(search.toLowerCase())
    );

  });

  if (loading) return <p>Loading requests...</p>;

  return (

    <div className="manager-card">

      <h2>👥 Team Leave Approvals</h2>

      <input
        type="text"
        placeholder="Search employee..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-box"
      />

      {filteredLeaves.length === 0 ? (

        <p>No leave requests found.</p>

      ) : (

        <table className="manager-table">

          <thead>
            <tr>
              <th>Employee</th>
              <th>Type</th>
              <th>From</th>
              <th>To</th>
              <th>Days</th>
              <th>Status</th>
              <th>Proof</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {filteredLeaves.map((leave) => (

              <tr key={leave.id}>

                <td>{leave.employee_name}</td>
                <td>{leave.leave_type}</td>
                <td>{leave.start_date}</td>
                <td>{leave.end_date}</td>
                <td>{leave.number_of_days}</td>

                <td>
                  <span className={`status-badge ${leave.status?.toLowerCase()}`}>
                    {leave.status}
                  </span>
                </td>
<td>
  {leave.proof_document ? (
    <a
      href={`http://localhost:8000/${leave.proof_document}`}
      target="_blank"
      rel="noreferrer"
    >
      View
    </a>
  ) : (
    "No Proof"
  )}
</td>
                <td>

                  <button
                    className="approve-btn"
                    onClick={() => {
                      setSelectedLeave(leave);
                      setActionType("approve");
                    }}
                  >
                    Approve
                  </button>

                  <button
                    className="reject-btn"
                    onClick={() => {
                      setSelectedLeave(leave);
                      setActionType("reject");
                    }}
                  >
                    Reject
                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      )}

      {/* 🔹 Confirmation Modal */}
      {selectedLeave && (

        <div className="modal-overlay">

          <div className="modal-box">

            <h3>
              Confirm {actionType === "approve" ? "Approval" : "Rejection"}
            </h3>

            <p>
              Are you sure you want to {actionType} leave for{" "}
              <strong>{selectedLeave.employee_name}</strong>?
            </p>

            <div className="modal-actions">

              <button onClick={() => setSelectedLeave(null)}>
                Cancel
              </button>

              <button
                className={
                  actionType === "approve"
                    ? "approve-btn"
                    : "reject-btn"
                }
                onClick={confirmAction}
              >
                Confirm
              </button>

            </div>

          </div>

        </div>

      )}

    </div>

  );

};

export default ManagerApprovals;