from app.services import user as user_service
from app.validators import users as validator
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


# List all users (Admin only)
@router.get("/users", response_model=list[validator.UserOut])
async def get_users(db: AsyncSession = Depends(get_db_session)):
    try:
        return await user_service.get_users(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching users.")


# Create new user (Admin only)
@router.post("/users", response_model=validator.UserOut)
async def create_user(user: validator.UserCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        user = await user_service.create_user(db, user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating user.")


# Get user by ID (Admin and User if self)
@router.get("/users/{user_id}", response_model=validator.UserOut)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_session)):
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching user.")


# Update user (Admin and User if self)
@router.put("/users/{user_id}", response_model=validator.UserOut)
async def update_user(user_id: int, user: validator.UserUpdate, db: AsyncSession = Depends(get_db_session)):
    try:
        updated_user = await user_service.update_user(db, user_id, user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating user.")


# Delete user (Admin only)
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    try:
        await user_service.delete_user(db, user_id)
        return {"detail": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting user.")
