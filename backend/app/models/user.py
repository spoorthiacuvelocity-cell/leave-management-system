from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from backend.database.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    gender = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    # Manager relationship
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # ================= RESIGNATION SYSTEM =================

    resignation_status = Column(String(20), nullable=True)
    # values: None / notice_period / resigned

    resignation_date = Column(Date, nullable=True)
    resignation_reason = Column(String, nullable=True)

    # Notice period start
    resignation_approval_date = Column(Date, nullable=True)

    # Last working day
    last_working_day = Column(Date, nullable=True)