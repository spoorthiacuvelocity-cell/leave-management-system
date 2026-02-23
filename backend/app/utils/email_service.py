import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.app.models.configuration import Configuration


# ================= GET CONFIG VALUE =================
def get_config_value(db: Session, key: str):
    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()

    return config.config_value if config else None


# ================= SEND EMAIL =================
def send_email(db: Session, to_email: str, subject: str, body: str):

    # ⚠️ Make sure DB keys match EXACTLY what you inserted
    sender_email = get_config_value(db, "MFA_EMAIL")
    sender_password = get_config_value(db, "MFA_EMAIL_PASSWORD")

    smtp_server = get_config_value(db, "SMTP_SERVER") or "smtp.gmail.com"
    smtp_port = int(get_config_value(db, "SMTP_PORT") or 587)

    if not sender_email or not sender_password:
        raise HTTPException(
            status_code=500,
            detail="Email configuration not found in database"
        )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())

        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Email sending failed"
        )
