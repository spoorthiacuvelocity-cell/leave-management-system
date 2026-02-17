import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from backend.app.models.configuration import Configuration


def send_email(db: Session, to_email: str, subject: str, body: str):
    # Get SMTP configuration from DB
    config = db.query(Configuration).filter(
        Configuration.leave_type == "SYSTEM"
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
