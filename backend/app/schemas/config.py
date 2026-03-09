from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConfigBase(BaseModel):
    config_parameter: str
    config_value: str


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(BaseModel):
    config_value: str


class ConfigResponse(ConfigBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    updated_by: Optional[str]

    class Config:
        orm_mode = True