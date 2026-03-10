from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import date
from sqlalchemy import func
from backend.app.models.configuration import Configuration
from backend.database.postgres import get_db
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.schemas.auth_schema import RegisterSchema
from backend.app.utils.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(request: RegisterSchema, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)

    new_user = User(
    name=request.name,
    email=request.email,
    password=hashed_password,
    role=request.role.upper(),
    gender=request.gender.upper(),
    manager_id=int(request.manager_id) if request.manager_id else None
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔥 Create default leave balances for new user
    default_leaves = [
        "CASUAL",
        "SICK",
        "EARNED",
        "LOSS_OF_PAY",
        "MATERNITY",
        "PATERNITY",
        "PERIODS"
    ]

    current_year = date.today().year
    current_quarter = (date.today().month - 1) // 3 + 1

    for leave_type in default_leaves:

        # Fetch leave limit from configuration table
        config = db.query(Configuration).filter(
        func.lower(Configuration.config_parameter) ==
        f"{leave_type.lower()}_quarter_limit"
        ).first()

        leave_limit = int(config.config_value) if config else 5
        balance = LeaveBalance(
            user_id=new_user.id,
            leave_type=leave_type,
            year=current_year,
            quarter=current_quarter,
            leaves_taken=0,
            remaining_leaves=leave_limit
        )

        db.add(balance)

    db.commit()

    return {"message": "User registered successfully"}


# =========================
# LOGIN
# =========================
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
    if not user.is_active:
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