import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session

from backend.app.models.configuration import Configuration


def get_config_value(db: Session, key: str):
    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()

    return config.config_value if config else None


def send_email(db: Session, to_email: str, subject: str, body: str):

    smtp_email = get_config_value(db, "mfa_email")
    smtp_password = get_config_value(db, "mfa_email_password")
    smtp_server = get_config_value(db, "smtp_server") or "smtp.gmail.com"
    smtp_port = int(get_config_value(db, "smtp_port") or 587)

    if not smtp_email or not smtp_password:
        raise Exception("Email configuration not set")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")
