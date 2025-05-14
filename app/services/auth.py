from jose import jwt
from sqlalchemy import select
from passlib.hash import bcrypt
from fastapi import HTTPException
from app.db.models.user import User
from sqlalchemy.orm import selectinload
import app.validators.auth as validator
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.jwt import create_access_token, create_refresh_token, decode_refresh_token


async def authenticate_user(db: AsyncSession, data: validator.LoginRequest):
    result = await db.execute(
        select(User).options(selectinload(User.role))
        .where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role.key,
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
