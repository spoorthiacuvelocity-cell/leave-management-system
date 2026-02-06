from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import auth, user, leave, admin, health


app = FastAPI(
    title="Leave Management System",
    version="1.0.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(leave.router)
app.include_router(admin.router)
app.include_router(health.router)


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Leave Management System Backend is running"}
