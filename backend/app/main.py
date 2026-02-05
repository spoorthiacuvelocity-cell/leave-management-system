## backend/app/main.py

from fastapi import FastAPI
from backend.routes import auth, user, leave, admin, health

app = FastAPI(title="Leave Management System")

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(leave.router, prefix="/leave", tags=["Leave"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
