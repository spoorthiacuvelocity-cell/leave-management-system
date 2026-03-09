import { useState } from "react";
import "../../styles/configuration.css";

export default function LeavePolicy() {
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [editIndex, setEditIndex] = useState(null);

  const [form, setForm] = useState({
    name: "",
    maxLeaves: "",
    carryForward: false,
    maxCarryForward: "",
    requiresApproval: true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = () => {
    if (!form.name || form.maxLeaves <= 0) return;

    if (editIndex !== null) {
      const updated = [...leaveTypes];
      updated[editIndex] = form;
      setLeaveTypes(updated);
      setEditIndex(null);
    } else {
      setLeaveTypes([...leaveTypes, form]);
    }

    setForm({
      name: "",
      maxLeaves: "",
      carryForward: false,
      maxCarryForward: "",
      requiresApproval: true,
    });
  };

  const handleEdit = (index) => {
    setForm(leaveTypes[index]);
    setEditIndex(index);
  };

  const handleDelete = (index) => {
    const updated = leaveTypes.filter((_, i) => i !== index);
    setLeaveTypes(updated);
  };

  return (
    <div>
      <div className="card">
        <h3>{editIndex !== null ? "Edit Leave Policy" : "Add Leave Policy"}</h3>

        <div className="input-group">
          <input
            name="name"
            placeholder="Leave Name"
            value={form.name}
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <input
            type="number"
            name="maxLeaves"
            placeholder="Max Leaves"
            value={form.maxLeaves}
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <label>
            <input
              type="checkbox"
              name="carryForward"
              checked={form.carryForward}
              onChange={handleChange}
            />
            Carry Forward
          </label>
        </div>

        {form.carryForward && (
          <div className="input-group">
            <input
              type="number"
              name="maxCarryForward"
              placeholder="Max Carry Forward"
              value={form.maxCarryForward}
              onChange={handleChange}
            />
          </div>
        )}

        <div className="input-group">
          <label>
            <input
              type="checkbox"
              name="requiresApproval"
              checked={form.requiresApproval}
              onChange={handleChange}
            />
            Requires Approval
          </label>
        </div>

        <button className="primary-btn" onClick={handleSubmit}>
          {editIndex !== null ? "Update" : "Add"}
        </button>
      </div>

      <div className="card">
        <h3>Leave Policies</h3>

        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Max</th>
              <th>Carry</th>
              <th>Approval</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {leaveTypes.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.maxLeaves}</td>
                <td>
                  {item.carryForward
                    ? `Yes (${item.maxCarryForward})`
                    : "No"}
                </td>
                <td>{item.requiresApproval ? "Yes" : "No"}</td>
                <td>
                  <button onClick={() => handleEdit(index)}>Edit</button>
                  <button
                    className="danger-btn"
                    onClick={() => handleDelete(index)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}