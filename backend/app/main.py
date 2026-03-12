from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database.postgres import SessionLocal, Base, engine
from backend.app.models.user import User
from backend.app.utils.auth_utils import hash_password

from backend.app.routes import auth, leave, dashboard, manager, admin, user
from backend.app.routes.configuration import router as config_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(dashboard.router)
app.include_router(manager.router)
app.include_router(admin.router)
app.include_router(config_router)
app.include_router(user.router)



# Create default admin
def create_default_admin():
    db = SessionLocal()

    admin = db.query(User).filter(User.email == "admin@gmail.com").first()

    if not admin:
        new_admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=hash_password("admin123"),
            role="ADMIN",
            gender="MALE",
            is_active=True
        )

        db.add(new_admin)
        db.commit()

    db.close()


@app.on_event("startup")
def startup_event():
    create_default_admin()