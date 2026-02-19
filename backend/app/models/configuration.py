from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP, Text, DateTime
from backend.database.postgres import Base
from sqlalchemy.sql import func
from datetime import datetime
class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    config_parameter = Column(String(255), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    updated_by = Column(String(100))
