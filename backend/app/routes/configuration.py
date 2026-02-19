from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.postgres import get_db
from backend.app.schemas.config import ConfigUpdate
from backend.app.models.configuration import Configuration
from backend.app.utils.auth_utils import get_current_user
from backend.app.models.user import User
from datetime import datetime

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


# ================= GET SINGLE CONFIG =================
@router.get("/{key}")
def get_config(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    return config


# ================= UPDATE CONFIG =================
@router.put("/{key}")
def update_config(
    key: str,
    request: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    config.config_value = request.config_value
    config.updated_at = datetime.utcnow()
    config.updated_by = current_user.email

    db.commit()

    return {"message": "Configuration updated successfully"}
