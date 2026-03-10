📌 Leave Management System

A role-based Leave Management System designed to streamline employee leave requests, approvals, and tracking within an organization.
The system enables Employees, Managers, and Admins to efficiently manage leave workflows with analytics, document uploads, and reporting features.

🚀 Features
👤 Employee

Apply for leave (Sick, Casual, Paternity, etc.)

Upload supporting documents (medical proof, etc.)

View leave history

Track leave status (Pending / Approved / Rejected)

Check leave balance

🧑‍💼 Manager

View team leave requests

Approve or reject employee leave

Provide remarks during approval/rejection

Monitor team leave activity

🛠 Admin

Manage employees and assign managers

View all leave requests

Approve or reject leaves

Access Leave Analytics Dashboard

Export leave reports as CSV

Filter reports by:

Month

Employee

Leave type

Preview uploaded documents

📊 Dashboard & Analytics

The system includes an Admin Analytics Dashboard showing:

📈 Leave trends by month

📊 Leave type distribution

📋 Employee leave summaries

📤 Exportable leave reports

These analytics help HR teams analyze leave patterns and workforce availability.

## 📂 Project Structure

```
leave-management-system
│
├── backend
│   ├── app
│   │   ├── models
│   │   ├── routes
│   │   ├── schemas
│   │   ├── service
│   │   └── utils
│   │
│   ├── database
│   └── main.py
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   ├── api
│   │   └── context
│
└── uploads
```

🛠 Tech Stack
Frontend

React.js

Axios

Chart.js (Analytics graphs)

CSS

Backend

FastAPI

SQLAlchemy

Pydantic

JWT Authentication

Database

PostgreSQL

Other Tools

Git & GitHub

Uvicorn

REST API

🔐 Authentication

The system uses JWT-based authentication to ensure secure access control.

Roles supported:

Employee

Manager

Admin

Each role has different permissions and dashboards.

📤 Document Upload

Employees can upload proof documents while applying for leave.

Examples:

Medical certificate

Hospital report

Other supporting documents

Admins and managers can preview uploaded files directly from the dashboard.

📥 Export Reports

Admins can download leave reports as CSV files, including:

All leave records

Filtered reports by month

Leave type based reports

Employee specific reports

⚙️ Installation
Clone Repository
git clone https://github.com/yourusername/leave-management-system.git
cd leave-management-system
Backend Setup
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload

Backend runs on:

http://localhost:8000

Swagger API docs:

http://localhost:8000/docs
Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs on:

http://localhost:5173
🌟 Key Highlights

✔ Role-based access control
✔ Leave approval workflow
✔ Leave analytics dashboard
✔ CSV report export
✔ Document upload & preview
✔ Manager-Employee hierarchy

👩‍💻 Author

Spoorthi D

📜 License

This project is for educational and internship purposes.
