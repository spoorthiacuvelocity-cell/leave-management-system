import { useEffect, useState } from "react";
import { getLeaveBalance } from "../../api/leaveApi";
import "../../styles/leaveBalance.css";

const LeaveBalance = () => {

  const [balance, setBalance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resignationApproved, setResignationApproved] = useState(false);

  useEffect(() => {

    const fetchBalance = async () => {

      try {

        const res = await getLeaveBalance();
        setBalance(res);

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

  if (balance.length === 0) {
    return <p>No leave balance found.</p>;
  }

  return (

    <div className="balance-container">

      <h2>Leave Balance</h2>

      <div className="balance-grid">

        {balance.map((item) => (

          <div key={item.leave_type} className="balance-card">

            <h3>{item.leave_type}</h3>

            <p><strong>Taken:</strong> {item.leaves_taken}</p>

            <p><strong>Remaining:</strong> {item.remaining_leaves}</p>

            <div className="progress-bar">

              <div
                className="progress-fill"
                style={{
                  width:`${(item.leaves_taken /
                    (item.leaves_taken + item.remaining_leaves || 1)) * 100}%`
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