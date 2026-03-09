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
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role.upper(),
        gender=user_data.gender.upper(),
        manager_id=user_data.manager_id,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create leave balance
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
@router.get("/managers")
def get_managers(db: Session = Depends(get_db)):

    managers = db.query(User).filter(User.role == "MANAGER").all()

    return [
        {
            "id": m.id,
            "name": m.name
        }
        for m in managers
    ]
# ---------------- GET ALL EMPLOYEES ----------------
@router.get("/employees")
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    employees = db.query(User).filter(User.role == "EMPLOYEE").all()

    return [
        {
            "id": e.id,
            "name": e.name,
            "email": e.email,
            "manager_id": e.manager_id,
            "is_active": e.is_active
        }
        for e in employees
    ]


# ---------------- UPDATE EMPLOYEE MANAGER ----------------
@router.put("/employees/{employee_id}/manager")
def update_employee_manager(
    employee_id: int,
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    employee = db.query(User).filter(User.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.manager_id = manager_id
    db.commit()

    return {"message": "Manager updated successfully"}


# ---------------- DEACTIVATE EMPLOYEE ----------------
@router.put("/employees/{employee_id}/deactivate")
def deactivate_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    employee = db.query(User).filter(User.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_active = False
    db.commit()

    return {"message": "Employee deactivated"}