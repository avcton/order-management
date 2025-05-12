from datetime import datetime
from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
