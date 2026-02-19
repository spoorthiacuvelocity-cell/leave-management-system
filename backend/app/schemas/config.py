from pydantic import BaseModel
from typing import Optional

class ConfigBase(BaseModel):
    config_parameter: str
    config_value: str

class ConfigCreate(ConfigBase):
    pass

class ConfigUpdate(BaseModel):
    config_value: str
    updated_by: Optional[str]

class ConfigResponse(ConfigBase):
    id: int

    class Config:
        orm_mode = True
