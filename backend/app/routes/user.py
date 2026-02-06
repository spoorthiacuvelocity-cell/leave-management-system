from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.user import User
from backend.app.models.leave_balance import LeaveBalance
from backend.app.schemas.user_schema import UserCreate
from backend.app.utils.auth_utils import hash_password, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ---------------- REGISTER USER ----------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # Create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        role="EMPLOYEE",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #  CREATE LEAVE BALANCE AUTOMATICALLY
    leave_balance = LeaveBalance(
        user_id=new_user.id
    )

    db.add(leave_balance)
    db.commit()

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ---------------- CURRENT USER PROFILE ----------------
@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }
