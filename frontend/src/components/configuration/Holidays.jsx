import { useState } from "react";
import "../../styles/configuration.css";

export default function Holidays() {
  const [holidays, setHolidays] = useState([]);
  const [form, setForm] = useState({
    name: "",
    date: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = () => {
    if (!form.name || !form.date) return;

    setHolidays([...holidays, form]);
    setForm({ name: "", date: "" });
  };

  const handleDelete = (index) => {
    const updated = holidays.filter((_, i) => i !== index);
    setHolidays(updated);
  };

  return (
    <div>
      <div className="card">
        <h3>Add Holiday</h3>

        <div className="input-group">
          <input
            name="name"
            placeholder="Holiday Name"
            value={form.name}
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <input
            type="date"
            name="date"
            value={form.date}
            onChange={handleChange}
          />
        </div>

        <button className="primary-btn" onClick={handleAdd}>
          Add Holiday
        </button>
      </div>

      <div className="card">
        <h3>Holiday List</h3>

        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {holidays.map((holiday, index) => (
              <tr key={index}>
                <td>{holiday.name}</td>
                <td>{holiday.date}</td>
                <td>
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