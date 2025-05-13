from jose import jwt
from app.config.settings import settings
from datetime import datetime, timedelta, timezone


def create_jwt_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        (expires_delta if expires_delta else timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY,
                      algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": True})
