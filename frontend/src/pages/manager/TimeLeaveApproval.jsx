import { useEffect, useState } from "react";
import {
  getTeamLeaves,
  approveLeaveByManager,
  rejectLeaveByManager,
} from "../../api/adminApi";

const TeamLeaveApprovals = () => {
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLeaves = async () => {
    const data = await getTeamLeaves();
    setLeaves(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  const approve = async (id) => {
    await approveLeaveByManager(id);
    fetchLeaves();
  };

  const reject = async (id) => {
    await rejectLeaveByManager(id);
    fetchLeaves();
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Team Leave Approvals (Project Manager)</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Dates</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {leaves.map((leave) => (
            <tr key={leave.id}>
              <td>{leave.user_name}</td>
              <td>{leave.start_date} → {leave.end_date}</td>
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

export default TeamLeaveApprovals;
