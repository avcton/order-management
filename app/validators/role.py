from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class RoleOut(BaseModel):
    id: int
    key: Role

    class Config:
        from_attributes = True
