import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from backend.app.models.leave_types import LeaveType
from backend.app.config import config
from fastapi import request
def send_email(db: Session, to_email: str, subject: str, body: str):
    # Get SMTP configuration from DB
    leave_type_config = db.query(LeaveType).filter(
    LeaveType.leave_name == request.leave_type
    ).first()
    if not config or not config.smtp_email:
        print("SMTP not configured in database")
        return

    smtp_email = config.smtp_email
    smtp_password = config.smtp_password
    smtp_server = config.smtp_server or "smtp.gmail.com"
    smtp_port = config.smtp_port or 587

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email sending failed:", str(e))
