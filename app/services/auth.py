from jose import jwt
from sqlalchemy import select
from passlib.hash import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
import app.validators.auth as validator
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from app.db.models import User, Role, RolePrivilege


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        (expires_delta if expires_delta else timedelta(
            minutes=settings.JWT_ACCESS_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        (expires_delta if expires_delta else timedelta(
            days=settings.JWT_REFRESH_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY,
                      algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": True})


def decode_refresh_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY,
                      algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": True})


async def authenticate_user(db: AsyncSession, data: validator.LoginRequest):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.role)
            .selectinload(Role.role_privileges)
            .selectinload(RolePrivilege.privilege)
        )
        .where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Extract privilege keys from the user's role
    privileges = [
        rp.privilege.key
        for rp in user.role.role_privileges
        if rp.privilege
    ]

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role.key,
        "privileges": privileges,
    })

    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def token_refresh(db: AsyncSession, refresh_request: validator.RefreshRequest):
    payload = decode_refresh_token(refresh_request.refresh_token)
    user_id = int(payload.get("sub")) if payload.get("sub") else None
    if not user_id:
        raise jwt.JWTError("Invalid refresh token")

    result = await db.execute(
        select(User).options(selectinload(User.role))
        .where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise jwt.JWTError("Invalid refresh token")

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role.key,
    })
    return {"access_token": access_token}
