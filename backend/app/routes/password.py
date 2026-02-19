from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from backend.database.postgres import get_db
from backend.app.models.user import User
from backend.app.models.password_reset import PasswordReset
from backend.app.utils.email_utils import send_email
from backend.app.utils.auth_utils import hash_password

router = APIRouter(
    prefix="/password",
    tags=["Password"]
)

# ---------------- REQUEST RESET ----------------
@router.post("/forgot")
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=30)

    reset_entry = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=expires
    )

    db.add(reset_entry)
    db.commit()

    reset_link = f"http://localhost:3000/reset-password/{token}"

    background_tasks.add_task(
        send_email,
        db,
        user.email,
        "Password Reset Request",
        f"Click this link to reset your password:\n{reset_link}"
    )

    return {"message": "Password reset email sent"}


# ---------------- RESET PASSWORD ----------------
@router.post("/reset/{token}")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):

    reset_record = db.query(PasswordReset).filter(
        PasswordReset.token == token
    ).first()

    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid token")

    if reset_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(User).filter(User.id == reset_record.user_id).first()

    user.password = hash_password(new_password)

    db.delete(reset_record)
    db.commit()

    return {"message": "Password reset successful"}
