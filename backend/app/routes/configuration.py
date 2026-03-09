from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database.postgres import get_db
from backend.app.models.configuration import Configuration
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.schemas.config import (
    ConfigCreate,
    ConfigUpdate,
    ConfigResponse
)
router = APIRouter(
    prefix="/admin/configuration",
    tags=["Configuration"]
)


# ================= GET ALL =================
@router.get("/", response_model=list[ConfigResponse])
def get_all_configurations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    return db.query(Configuration).all()


# ================= ADD =================
@router.post("/", response_model=ConfigResponse)
def add_configuration(
    request: ConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    existing = db.query(Configuration).filter(
        Configuration.config_parameter == request.config_parameter
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Parameter already exists")

    config = Configuration(
        config_parameter=request.config_parameter,
        config_value=request.config_value,
        updated_by=current_user.name
    )

    db.add(config)
    db.commit()
    db.refresh(config)

    return config
# ================= UPDATE =================
@router.put("/{config_id}", response_model=ConfigResponse)
def update_configuration(
    config_id: int,
    request: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    config = db.query(Configuration).filter(
        Configuration.id == config_id
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    # Update fields
    config.config_value = request.config_value
    config.updated_by = current_user.name
    config.updated_at = datetime.now()   # 🔥 Add this line

    db.commit()
    db.refresh(config)

    return config
@router.delete("/{config_id}")
def delete_configuration(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    config = db.query(Configuration).filter(
        Configuration.id == config_id
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    db.delete(config)
    db.commit()

    return {"message": "Configuration deleted successfully"}