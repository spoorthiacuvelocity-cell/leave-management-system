import { useEffect, useState } from "react";
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
    const res = await fetch("http://localhost:8000/users/managers");
    const data = await res.json();
    setManagers(data);
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

  return (

    <div style={{ padding: "30px" }}>

      <h2>Employee Management</h2>

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