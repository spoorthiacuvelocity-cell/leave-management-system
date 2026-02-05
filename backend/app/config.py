# app/config.py

import os
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgre123@localhost:5432/leave-management"
)


class Settings:
    # Environment
    ENV: str = os.getenv("ENV", "dev")

    # Database (Cloud SQL / Local)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:password@localhost:5432/leave_db"
    )

    # Security (we'll use later)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
