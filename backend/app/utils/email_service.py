import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from backend.app.models.configuration import Configuration


def get_email_config(db: Session):
    email = db.query(Configuration).filter(
        Configuration.config_parameter == "MFA_EMAIL"
    ).first()

    password = db.query(Configuration).filter(
        Configuration.config_parameter == "MFA_EMAIL_PASSWORD"
    ).first()

    if not email or not password:
        raise Exception("Email configuration not found in database")

    return email.config_value, password.config_value


def send_email(db: Session, to_email: str, subject: str, body: str):

    sender_email, sender_password = get_email_config(db)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", str(e))
