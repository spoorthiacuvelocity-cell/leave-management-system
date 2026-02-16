from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from backend.database.postgres import get_db
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.schemas.auth_schema import RegisterSchema, LoginSchema
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
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = User(
        email=request.email,
        password=hash_password(request.password),
        role=request.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Create default leave balance
    default_balance = LeaveBalance(
    leave_type="Sick Leave",
    total_days=10,
    user_id=new_user.id
    )

    db.add(default_balance)
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
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

