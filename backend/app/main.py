from fastapi import FastAPI
from backend.database.postgres import Base, engine
from backend.app.routes import auth, leave, configuration, admin
from backend.app.routes import manager
from backend.app.routes import password
from backend.app.routes import dashboard
from backend.app.routes import resignation
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(configuration.router)
app.include_router(manager.router)
app.include_router(password.router)
app.include_router(dashboard.router)
app.include_router(admin.router)
app.include_router(resignation.router)