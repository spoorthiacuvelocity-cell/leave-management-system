import { useState } from "react";
import { applyLeave } from "../../api/leaveApi";

const ApplyLeave = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      await applyLeave({
        start_date: startDate,
        end_date: endDate,
        reason: reason,
      });

      setMessage("Leave applied successfully");
      setStartDate("");
      setEndDate("");
      setReason("");
    } catch (err) {
      setError("Failed to apply leave");
    }
  };

  return (
    <div>
      <h2>Apply Leave</h2>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <label>Start Date</label><br />
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
        <br /><br />

        <label>End Date</label><br />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          required
        />
        <br /><br />

        <label>Reason</label><br />
        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          required
        />
        <br /><br />

        <button type="submit">Apply Leave</button>
      </form>
    </div>
  );
};

export default ApplyLeave;
