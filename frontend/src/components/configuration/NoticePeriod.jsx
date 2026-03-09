import { useState } from "react";
import "../../styles/configuration.css";

export default function NoticePeriod() {
  const [notice, setNotice] = useState({
    noticeDays: 30,
    allowLeaveDuringNotice: false,
    autoDeductBalance: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNotice({
      ...notice,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSave = () => {
    if (notice.noticeDays <= 0) return;
    alert("Notice configuration saved (frontend mode)");
  };

  return (
    <div className="card">
      <h3>Notice Period Configuration</h3>

      <div className="input-group">
        <input
          type="number"
          name="noticeDays"
          placeholder="Notice Period (Days)"
          value={notice.noticeDays}
          onChange={handleChange}
        />
      </div>

      <div className="input-group">
        <label>
          <input
            type="checkbox"
            name="allowLeaveDuringNotice"
            checked={notice.allowLeaveDuringNotice}
            onChange={handleChange}
          />
          Allow Leave During Notice Period
        </label>
      </div>

      <div className="input-group">
        <label>
          <input
            type="checkbox"
            name="autoDeductBalance"
            checked={notice.autoDeductBalance}
            onChange={handleChange}
          />
          Auto Deduct Leave Balance
        </label>
      </div>

      <button className="primary-btn" onClick={handleSave}>
        Save
      </button>
    </div>
  );
}