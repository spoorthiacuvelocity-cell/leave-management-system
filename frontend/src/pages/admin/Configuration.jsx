import { useEffect, useState } from "react";
import {
  getConfigurations,
  addConfiguration,
  updateConfiguration,
  deleteConfiguration,
} from "../../api/configurationApi";

import "../../styles/admin.css";

const Configuration = () => {
  const [configs, setConfigs] = useState([]);
  const [newParam, setNewParam] = useState("");
  const [newValue, setNewValue] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editValue, setEditValue] = useState("");

  const fetchConfigs = async () => {
    const res = await getConfigurations();
    setConfigs(res.data);
  };

  useEffect(() => {
    fetchConfigs();
  }, []);

  const handleAdd = async () => {
    if (!newParam || !newValue) {
      alert("Fill all fields");
      return;
    }

    await addConfiguration({
      config_parameter: newParam,
      config_value: newValue,
    });

    setNewParam("");
    setNewValue("");
    fetchConfigs();
  };

  const startEdit = (config) => {
    setEditingId(config.id);
    setEditValue(config.config_value);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditValue("");
  };

  const saveEdit = async (id) => {
    await updateConfiguration(id, {
      config_value: editValue,
    });
    setEditingId(null);
    fetchConfigs();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this configuration?")) return;
    await deleteConfiguration(id);
    fetchConfigs();
  };

  return (
    <div className="admin-card">
      <h2>⚙ Configuration Management</h2>

      <div className="config-add">
        <input
          placeholder="Parameter"
          value={newParam}
          onChange={(e) => setNewParam(e.target.value)}
        />
        <input
          placeholder="Value"
          value={newValue}
          onChange={(e) => setNewValue(e.target.value)}
        />
        <button onClick={handleAdd}>Add</button>
      </div>

      <table className="admin-table">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Value</th>
            <th>Updated By</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {configs.map((config) => (
            <tr key={config.id}>
              <td>{config.config_parameter}</td>

              <td>
                {editingId === config.id ? (
                  <input
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                  />
                ) : (
                  config.config_value
                )}
              </td>

              <td>{config.updated_by || "—"}</td>

              <td>
                {config.created_at
                  ? new Date(config.created_at).toLocaleString()
                  : "—"}
              </td>

              <td>
                {config.updated_at
                  ? new Date(config.updated_at).toLocaleString()
                  : "—"}
              </td>

              <td>
  <div className="action-buttons">
    {editingId === config.id ? (
      <>
        <button
          className="btn save-btn"
          onClick={() => saveEdit(config.id)}
        >
          Save
        </button>
        <button
          className="btn cancel-btn"
          onClick={cancelEdit}
        >
          Cancel
        </button>
      </>
    ) : (
      <>
        <button
          className="btn edit-btn"
          onClick={() => startEdit(config)}
        >
          Edit
        </button>
        <button
          className="btn delete-btn"
          onClick={() => handleDelete(config.id)}
        >
          Delete
        </button>
      </>
    )}
  </div>
</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Configuration;