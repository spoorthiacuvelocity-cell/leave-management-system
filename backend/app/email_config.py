from fastapi_mail import ConnectionConfig
from backend.app.config import (
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_FROM_NAME
)

conf = ConnectionConfig(
    MAIL_USERNAME="acumenleavesystem@gmail.com",
    MAIL_PASSWORD="vtloxzxvheosfmsp",
    MAIL_FROM="acumenleavesystem@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="AcumenLeaveSystem",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)