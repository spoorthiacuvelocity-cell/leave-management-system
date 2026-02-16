from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from backend.database.postgres import Base
from sqlalchemy.sql import func


class Configuration(Base):
    __tablename__ = "configuration"

    config_id = Column(Integer, primary_key=True, index=True)
    leave_type = Column(String(30), unique=True)
    leaves_per_quarter = Column(Numeric(3, 1))
    max_consecutive_leaves = Column(Integer)
    notice_period_days = Column(Integer, default=0)
    proof_required = Column(Boolean, default=False)
    proof_required_after_days = Column(Integer)
    gender_specific = Column(String(10))
    resignation_notice_period_days = Column(Integer, default=60)
    created_at = Column(TIMESTAMP, server_default=func.now())
