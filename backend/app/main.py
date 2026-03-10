from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database.postgres import Base, engine

from backend.app.routes import auth, leave, dashboard
from backend.app.routes import manager
from backend.app.routes import resignation
from backend.app.routes import admin
from backend.app.routes import user
from backend.app.routes.configuration import router as config_router


app = FastAPI()

# Serve uploaded documents
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",  # React dev server
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(dashboard.router)
app.include_router(manager.router)
app.include_router(resignation.router)
app.include_router(admin.router)
app.include_router(config_router)
app.include_router(user.router)