import { useEffect, useState } from "react";
import API from "../../api/axiosInstance";
import {
  getEmployees,
  updateEmployeeManager,
  deactivateEmployee
} from "../../api/adminUserApi";

const EmployeeManagement = () => {

  const [employees, setEmployees] = useState([]);
  const [managers, setManagers] = useState([]);

  const fetchEmployees = async () => {
    const res = await getEmployees();
    setEmployees(res.data);
  };

  const fetchManagers = async () => {
    const res = await API.get("/users/managers");
    setManagers(res.data);
  };

  useEffect(() => {
    fetchEmployees();
    fetchManagers();
  }, []);

  const handleManagerChange = async (employeeId, managerId) => {
    await updateEmployeeManager(employeeId, managerId);
    fetchEmployees();
  };

  const handleDeactivate = async (employeeId) => {
    await deactivateEmployee(employeeId);
    fetchEmployees();
  };

  // ✅ Export CSV
  const exportCSV = async () => {
    try {

      const response = await API.get("/admin/export-leaves", {
        responseType: "blob"
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "leaves.csv");

      document.body.appendChild(link);
      link.click();
      link.remove();

    } catch (error) {
      console.error("Export failed", error);
    }
  };

  return (

    <div style={{ padding: "30px" }}>

      <h2>Employee Management</h2>

      {/* ✅ Export button (only once) */}
      <button
        onClick={exportCSV}
        style={{ marginBottom: "15px" }}
      >
        Export CSV
      </button>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Manager</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>

          {employees.map((emp) => (

            <tr key={emp.id}>

              <td>{emp.name}</td>
              <td>{emp.email}</td>

              <td>
                <select
                  value={emp.manager_id || ""}
                  onChange={(e) =>
                    handleManagerChange(emp.id, e.target.value)
                  }
                >
                  <option value="">No Manager</option>

                  {managers.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.name}
                    </option>
                  ))}

                </select>
              </td>

              <td>
                <span
                  style={{
                    color: emp.is_active ? "green" : "red",
                    fontWeight: "bold"
                  }}
                >
                  {emp.is_active ? "Active" : "Inactive"}
                </span>
              </td>

              <td>
                <button
                  disabled={!emp.is_active}
                  onClick={() => handleDeactivate(emp.id)}
                >
                  Deactivate
                </button>
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

};

export default EmployeeManagement;