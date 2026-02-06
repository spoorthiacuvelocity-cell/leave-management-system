# backend/routes/admin.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard():
    return {"message": "Admin dashboard"}
