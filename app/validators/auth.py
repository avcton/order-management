from pydantic import BaseModel, model_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    def lowercase_fields(self):
        self.username = self.username.lower()
        return self
