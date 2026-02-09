import { useEffect, useState } from "react";
import {
  getAllLeaves,
  approveLeaveByAdmin,
  rejectLeaveByAdmin,
} from "../../api/adminApi";

const AllLeaveApprovals = () => {
  const [leaves, setLeaves] = useState([]);

  const fetchLeaves = async () => {
    const data = await getAllLeaves();
    setLeaves(data);
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  const approve = async (id) => {
    await approveLeaveByAdmin(id);
    fetchLeaves();
  };

  const reject = async (id) => {
    await rejectLeaveByAdmin(id);
    fetchLeaves();
  };

  return (
    <div>
      <h2>All Leave Approvals (Admin)</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Approved By</th>
            <th>Status</th>
            <th>Final Action</th>
          </tr>
        </thead>
        <tbody>
          {leaves.map((leave) => (
            <tr key={leave.id}>
              <td>{leave.user_name}</td>
              <td>{leave.approved_by_role || "—"}</td>
              <td>{leave.status}</td>
              <td>
                <button onClick={() => approve(leave.id)}>Approve</button>
                <button onClick={() => reject(leave.id)} style={{ marginLeft: 8 }}>
                  Reject
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AllLeaveApprovals;
