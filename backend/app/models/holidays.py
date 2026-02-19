from sqlalchemy import Column, Integer, String, Date
from backend.database.postgres import Base


class Holiday(Base):
    __tablename__ = "holiday"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, unique=True)
