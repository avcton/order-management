from sqlalchemy import select
from passlib.hash import bcrypt
from fastapi import HTTPException
from app.db.models.user import User
from sqlalchemy.orm import selectinload
from app.validators.auth import LoginRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.jwt import create_jwt_token, decode_jwt_token


async def authenticate_user(db: AsyncSession, data: LoginRequest):
    result = await db.execute(
        select(User).options(selectinload(User.role))
        .where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({
        "sub": str(user.id),
        "role": user.role.key,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }
