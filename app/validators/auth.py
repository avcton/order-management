from pydantic import BaseModel, model_validator


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class AccessTokenData(BaseModel):
    sub: str
    role: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    def lowercase_fields(self):
        self.username = self.username.lower()
        return self
