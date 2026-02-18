from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP, Text
from backend.database.postgres import Base
from sqlalchemy.sql import func


class Configuration(Base):
    __tablename__ = "configuration"

    config_id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_on = Column(TIMESTAMP, nullable=True)
    updated_by = Column(String(100), nullable=True)

    # 🔥 NEW EMAIL SETTINGS
    smtp_email = Column(String, nullable=True)
    smtp_password = Column(String, nullable=True)
    smtp_server = Column(String, default="smtp.gmail.com")
    smtp_port = Column(Integer, default=587)
