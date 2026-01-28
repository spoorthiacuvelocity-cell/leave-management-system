from fastapi import FastAPI
from database import engine
import models
from routes.leave import router as leave_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(leave_router)

@app.get("/")
def root():
    return {"message": "FastAPI is running"}