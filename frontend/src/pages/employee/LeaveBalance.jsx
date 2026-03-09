import { useEffect, useState } from "react";
import { getLeaveBalance } from "../../api/leaveApi";
import "../../styles/leaveBalance.css";

const LeaveBalance = () => {

  const [balance, setBalance] = useState({});
  const [loading, setLoading] = useState(true);
  const [resignationApproved, setResignationApproved] = useState(false);

  useEffect(() => {

    const fetchBalance = async () => {

      try {

        const res = await getLeaveBalance();
        setBalance(res.data);

      } catch (error) {

        if (error.response?.status === 403) {
          setResignationApproved(true);
        } else {
          console.log(error);
        }

      } finally {
        setLoading(false);
      }

    };

    fetchBalance();

  }, []);

  if (loading) return <p>Loading Leave Balance...</p>;

  if (resignationApproved) {

    return (

      <div className="balance-container">

        <h2>Leave Balance</h2>

        <div style={{
          background:"#f8d7da",
          padding:"25px",
          borderRadius:"8px",
          color:"#721c24"
        }}>
          Your resignation has been approved.  
          Leave balance is no longer available.
        </div>

      </div>

    );

  }

  const leaveTypes = Object.keys(balance);

  if (leaveTypes.length === 0) {
    return <p>No leave balance found.</p>;
  }

  return (

    <div className="balance-container">

      <h2>Leave Balance</h2>

      <div className="balance-grid">

        {leaveTypes.map((type) => (

          <div key={type} className="balance-card">

            <h3>{type.toUpperCase()}</h3>

            <p><strong>Taken:</strong> {balance[type].taken}</p>

            <p><strong>Remaining:</strong> {balance[type].remaining}</p>

            <div className="progress-bar">

              <div
                className="progress-fill"
                style={{
                  width:`${(balance[type].taken /
                    (balance[type].taken + balance[type].remaining)) * 100}%`
                }}
              ></div>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

};

export default LeaveBalance;