from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.postgres import get_db
from backend.app.schemas.config import ConfigUpdate
from backend.app.models.configuration import Configuration
from backend.app.utils.auth_utils import get_current_user
from backend.app.models.user import User

router = APIRouter(
    prefix="/config",
    tags=["Configuration"]
)

# ================= VIEW ALL CONFIG =================
@router.get("/")
def get_all_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(Configuration).all()


# ================= UPDATE CONFIG =================
@router.put("/update/{leave_type}")
def update_config(
    leave_type: str,
    request: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    config = db.query(Configuration).filter(
        Configuration.leave_type == leave_type.upper()
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Leave type not found")

    # Leave Settings
    if request.leaves_per_quarter is not None:
        config.leaves_per_quarter = request.leaves_per_quarter

    if request.max_consecutive_leaves is not None:
        config.max_consecutive_leaves = request.max_consecutive_leaves

    if request.notice_period_days is not None:
        config.notice_period_days = request.notice_period_days

    if request.proof_required is not None:
        config.proof_required = request.proof_required

    if request.proof_required_after_days is not None:
        config.proof_required_after_days = request.proof_required_after_days

    # 🔥 Email Settings
    if request.smtp_email is not None:
        config.smtp_email = request.smtp_email

    if request.smtp_password is not None:
        config.smtp_password = request.smtp_password

    if request.smtp_server is not None:
        config.smtp_server = request.smtp_server

    if request.smtp_port is not None:
        config.smtp_port = request.smtp_port

    db.commit()

    return {"message": "Configuration updated successfully"}
