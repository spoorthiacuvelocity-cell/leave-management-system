import "../../styles/leaveApply.css";
import { applyLeave, getLeaveTypes } from "../../api/leaveApi";
import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
const EmployeeLeave = () => {

  const auth = useAuth();
  const user = auth?.user;

  const [formData, setFormData] = useState({
    leave_type: "",
    start_date: "",
    end_date: "",
    reason: "",
    proof_document: null
  });

  const [days, setDays] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [blocked, setBlocked] = useState(false);

  const today = new Date().toISOString().split("T")[0];

  // ================= LOAD LEAVE TYPES =================
  useEffect(() => {

    getLeaveTypes()
      .then((res) => {
        if (Array.isArray(res.data)) {
          setLeaveTypes(res.data);
        } else {
          setLeaveTypes([]);
        }
      })
      .catch((err) => {
        console.log("Error fetching leave types:", err);
        setLeaveTypes([]);
      });

  }, []);

  // ================= FILTER BASED ON GENDER =================
  const filteredLeaveTypes = Array.isArray(leaveTypes)
    ? leaveTypes.filter((type) => {

        if (!user || !user.gender) return true;

        const gender = user.gender.toUpperCase();

        if (gender === "MALE") {
          return type !== "MATERNITY" && type !== "PERIODS";
        }

        if (gender === "FEMALE") {
          return type !== "PATERNITY";
        }

        return true;

      })
    : [];

  // ================= HANDLE INPUT =================
  const handleChange = (e) => {

    const { name, value } = e.target;

    const updatedData = {
      ...formData,
      [name]: value
    };

    setFormData(updatedData);

    if (updatedData.start_date && updatedData.end_date) {

      const start = new Date(updatedData.start_date);
      const end = new Date(updatedData.end_date);

      if (end >= start) {

        const diffDays =
          (end - start) / (1000 * 60 * 60 * 24) + 1;

        setDays(diffDays);

      } else {
        setDays(0);
      }

    }

  };

  // ================= FILE UPLOAD =================
  const handleFileChange = (e) => {

    setFormData({
      ...formData,
      proof_document: e.target.files[0]
    });

  };

  // ================= SUBMIT LEAVE =================
  const handleSubmit = async (e) => {

    e.preventDefault();

    if (blocked) return;

    if (!formData.leave_type || !formData.start_date || !formData.end_date) {
      setMessage({
        type: "error",
        text: "Please fill all required fields."
      });
      return;
    }

    try {

      setLoading(true);
      setMessage(null);

      const form = new FormData();

      form.append("leave_type", formData.leave_type);
      form.append("start_date", formData.start_date);
      form.append("end_date", formData.end_date);
      form.append("reason", formData.reason);

      if (formData.proof_document) {
        form.append("proof_document", formData.proof_document);
      }

      await applyLeave(form);

      setMessage({
        type: "success",
        text: "Leave applied successfully!"
      });

      setFormData({
        leave_type: "",
        start_date: "",
        end_date: "",
        reason: "",
        proof_document: null
      });

      setDays(0);

    } catch (error) {

      console.log(error);

      if (error.response?.status === 403) {
        setBlocked(true);
      }

      setMessage({
        type: "error",
        text: error.response?.data?.detail || "Failed to apply leave."
      });

    } finally {

      setLoading(false);

    }

  };

  // ================= BLOCKED STATE =================
  if (blocked) {

    return (

      <div className="leave-apply-card">

        <h2>📅 Apply Leave</h2>

        <div
          style={{
            background: "#f8d7da",
            padding: "25px",
            borderRadius: "8px",
            color: "#721c24"
          }}
        >
          Your resignation has been approved.
          Leave requests are disabled.
        </div>

      </div>

    );

  }

  return (

    <div className="leave-apply-card">

      <h2>📅 Apply Leave</h2>

      {message && (
        <div className={`leave-alert ${message.type}`}>
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="leave-form">

        <div className="form-row">

          <div className="form-group">

            <label>Leave Type</label>

            <select
              name="leave_type"
              value={formData.leave_type}
              onChange={handleChange}
              required
            >
              <option value="">Select Leave Type</option>

              {filteredLeaveTypes.map((type) => (
                <option key={type} value={type}>
                  {type.replace(/_/g, " ")}
                </option>
              ))}

            </select>

          </div>

          <div className="days-badge">
            {days > 0 && <span>{days} Day(s)</span>}
          </div>

        </div>

        <div className="form-row">

          <div className="form-group">

            <label>Start Date</label>

            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              min={today}
              max={formData.leave_type === "SICK" ? today : undefined}
              required
            />

          </div>

          <div className="form-group">

            <label>End Date</label>

            <input
              type="date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              min={formData.start_date || today}
              required
            />

          </div>

        </div>

        <div className="form-group full-width">

          <label>Reason</label>

          <textarea
            name="reason"
            value={formData.reason}
            onChange={handleChange}
            rows="3"
          />

        </div>

        <div className="form-group full-width">

          <label>Proof Document (Optional)</label>

          <input
            type="file"
            name="proof_document"
            accept=".pdf,.jpg,.png"
            onChange={handleFileChange}
          />

        </div>

        <button
          type="submit"
          className="submit-btn"
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit Leave Request"}
        </button>

      </form>

    </div>

  );

};

export default EmployeeLeave;