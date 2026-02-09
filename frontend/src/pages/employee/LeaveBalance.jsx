const LeaveBalance = () => {
  // Dummy data for now (API later)
  const leaveBalance = {
    totalLeaves: 20,
    usedLeaves: 6,
    remainingLeaves: 14,
  };

  return (
    <div>
      <h2>Leave Balance</h2>

      <table border="1" cellPadding="10">
        <tbody>
          <tr>
            <th>Total Leaves</th>
            <td>{leaveBalance.totalLeaves}</td>
          </tr>
          <tr>
            <th>Used Leaves</th>
            <td>{leaveBalance.usedLeaves}</td>
          </tr>
          <tr>
            <th>Remaining Leaves</th>
            <td>{leaveBalance.remainingLeaves}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default LeaveBalance;
