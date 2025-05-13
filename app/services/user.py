from passlib.hash import bcrypt
from app.db.models import User, Role
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.validators import users as validator
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user_data: validator.UserCreate):
    # Check for existing email
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    # Check for existing username
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise ValueError("Username already taken")

    # Check if role exists
    result = await db.execute(select(Role).where(Role.key == user_data.role))
    role = result.scalar_one_or_none()
    if not role:
        raise ValueError("Role not found")

    hashed_password = bcrypt.hash(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=role
    )

    db.add(user)
    await db.flush()  # Auto populate user_id
    return user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.role)))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).options(selectinload(User.role)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: int, user_data: validator.UserUpdate):
    # Get the user
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    # Check and update password
    if user_data.password:
        hashed_password = bcrypt.hash(user_data.password)
        user.hashed_password = hashed_password

    # Check and update username
    if user_data.username and user_data.username != user.username:
        result = await db.execute(
            select(User).where(User.username ==
                               user_data.username, User.id != user.id)
        )
        if result.scalar_one_or_none():
            raise ValueError("Username already taken")
        user.username = user_data.username

    # Check and update email
    if user_data.email and user_data.email != user.email:
        result = await db.execute(
            select(User).where(User.email ==
                               user_data.email, User.id != user.id)
        )
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")
        user.email = user_data.email

    # Check and update role
    if user_data.role:
        result = await db.execute(select(Role).where(Role.key == user_data.role))
        role = result.scalar_one_or_none()
        if not role:
            raise ValueError("Role not found")
        user.role = role

    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    await db.delete(user)
    await db.flush()
