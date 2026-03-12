from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import date
from fastapi_mail import FastMail, MessageSchema
from passlib.context import CryptContext

from backend.database.postgres import SessionLocal, get_db
from backend.app.models.user import User
from backend.app.schemas.auth_schema import ForgotPasswordSchema, ResetPasswordSchema
from backend.app.utils.token import create_reset_token, verify_reset_token
from backend.app.utils.auth_utils import verify_password, create_access_token
from backend.app.email_config import conf

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ================= LOGIN =================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    today = date.today()

    if user.resignation_status == "notice_period":

        if user.last_working_day and today > user.last_working_day:

            user.resignation_status = "resigned"
            user.is_active = False
            db.commit()

            raise HTTPException(
                status_code=403,
                detail="Your employment has ended."
            )

    if user.resignation_status == "resigned" or not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="Your account has been deactivated. Contact admin."
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "gender": user.gender,
        "name": user.name
    }


# ================= FORGOT PASSWORD =================
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):

    db = SessionLocal()

    try:

        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token = create_reset_token(data.email)

        reset_link = f"http://localhost:5173/reset-password/{token}"

        html = f"""
        <html>
        <body style="font-family: Arial; background:#f4f6f8; padding:20px;">
            <div style="max-width:500px; background:white; padding:30px;
                        border-radius:8px; margin:auto; text-align:center;">

                <h2>Reset Your Password</h2>

                <p>Hello {user.name},</p>

                <p>You requested to reset your password.</p>

                <a href="{reset_link}" 
                   style="display:inline-block;padding:12px 20px;
                   background:#1976d2;color:white;text-decoration:none;
                   border-radius:5px;font-weight:bold;">
                   Reset Password
                </a>

                <p style="margin-top:20px;">
                    If you did not request this, please ignore this email.
                </p>

            </div>
        </body>
        </html>
        """

        message = MessageSchema(
            subject="Reset Your Password",
            recipients=[data.email],
            body=html,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        return {"message": "Password reset link sent"}

    finally:
        db.close()


# ================= RESET PASSWORD =================
@router.post("/reset-password")
def reset_password(data: ResetPasswordSchema):

    db = SessionLocal()

    try:

        try:
            email = verify_reset_token(data.token)
        except:
            raise HTTPException(status_code=400, detail="Reset link expired or invalid")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = pwd_context.hash(data.new_password)

        db.commit()

        return {"message": "Password reset successful"}

    finally:
        db.close()