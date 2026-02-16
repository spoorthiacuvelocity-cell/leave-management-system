from fastapi_mail import FastMail, MessageSchema
from .email_config import conf

async def send_email(subject: str, recipients: list, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
