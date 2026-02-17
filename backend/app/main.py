from fastapi import FastAPI
from backend.database.postgres import Base, engine
from backend.app.routes import auth, leave, configuration
from backend.app.routes import manager
from backend.app.routes import password
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(configuration.router)
app.include_router(manager.router)
app.include_router(password.router)
