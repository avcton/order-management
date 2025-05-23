from enum import Enum
from app.validators.role import Role
from pydantic import BaseModel, model_validator


class TokenType(str, Enum):
    BEARER = "Bearer"


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: TokenType = TokenType.BEARER


class AccessTokenData(BaseModel):
    sub: str
    role: Role
    privileges: list[str]


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: TokenType = TokenType.BEARER


class LoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    def lowercase_fields(self):
        self.username = self.username.lower()
        return self
