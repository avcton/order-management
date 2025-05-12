from datetime import datetime
from app.validators.role import RoleOut
from app.validators.passwords import PasswordStr
from pydantic import BaseModel, EmailStr, model_validator


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleOut
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: PasswordStr
    role: str

    @model_validator(mode="after")
    def lowercase_fields(self):
        self.username = self.username.lower()
        self.email = self.email.lower()
        self.role = self.role.lower()
        return self


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: PasswordStr | None = None
    role: str | None = None

    @model_validator(mode="after")
    def lowercase_fields(self):
        if self.username:
            self.username = self.username.lower()
        if self.email:
            self.email = self.email.lower()
        if self.role:
            self.role = self.role.lower()
        return self
