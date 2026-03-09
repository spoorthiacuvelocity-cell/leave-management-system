import { useState, useEffect } from "react";
import "../../styles/resignation.css";
import { applyResignation, getMyResignation } from "../../api/resignationApi";

const EmployeeResignation = () => {

  const [form, setForm] = useState({
    reason: "",
    last_working_day: "",
  });

  const [showConfirm, setShowConfirm] = useState(false);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {

    const fetchStatus = async () => {

      try {

        const res = await getMyResignation();

        if (res.data.status) {
          setStatus(res.data.status);
        }

      } catch (error) {

        if (error.response?.status === 403) {
          setErrorMessage(error.response.data.detail);
        } else {
          console.error("Error fetching resignation status:", error);
        }

      }

    };

    fetchStatus();

  }, []);

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });

  };

  const handleSubmit = async () => {

    setShowConfirm(false);
    setLoading(true);

    try {

      await applyResignation({
        reason: form.reason,
        last_working_day: form.last_working_day,
      });

      setStatus("PENDING");

    } catch (error) {

      alert(
        error?.response?.data?.detail ||
        "Failed to submit resignation"
      );

    }

    setLoading(false);

  };

  return (

    <div className="resignation-card">

      <div className="resignation-header">
        <h2>⚠ Apply Resignation</h2>

        {status && (
          <span className={`status-badge ${status.toLowerCase()}`}>
            {status}
          </span>
        )}

      </div>

      {errorMessage && (
        <p style={{ color: "red", marginBottom: "15px" }}>
          {errorMessage}
        </p>
      )}

      {!status && !errorMessage && (
        <>

          <div className="resignation-field">
            <label>Last Working Day</label>

            <input
              type="date"
              name="last_working_day"
              value={form.last_working_day}
              onChange={handleChange}
              required
            />

          </div>

          <div className="resignation-field">
            <label>Reason</label>

            <textarea
              name="reason"
              rows="4"
              placeholder="Enter reason for resignation..."
              value={form.reason}
              onChange={handleChange}
              required
            />

          </div>

          <button
            className="resignation-btn"
            onClick={() => setShowConfirm(true)}
            disabled={loading}
          >
            Submit Resignation
          </button>

        </>
      )}

      {loading && <div className="loader"></div>}

      {status === "PENDING" && (
        <div className="hr-status">
          ⏳ HR Approval Status: <strong>Awaiting Approval</strong>
        </div>
      )}

      {status === "APPROVED" && (
        <div className="hr-status approved">
          ✅ Your resignation has been approved
        </div>
      )}

      {showConfirm && (

        <div className="modal-overlay">

          <div className="modal-box">

            <h3>Confirm Resignation</h3>

            <p>
              Are you sure you want to submit your resignation?
              This action cannot be undone.
            </p>

            <div className="modal-actions">

              <button onClick={() => setShowConfirm(false)}>
                Cancel
              </button>

              <button
                className="confirm-btn"
                onClick={handleSubmit}
                disabled={loading}
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

export default EmployeeResignation;