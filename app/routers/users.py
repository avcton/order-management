from app.services import user as user_service
from app.validators import users as validator
from app.config.database import get_db_session
from app.validators.auth import AccessTokenData
from app.services import order as order_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.router import get_api_router
from fastapi import Depends, HTTPException, Request
from app.validators import orders as order_validator

router = get_api_router("users")


# Create new user (Admin only)
@router.post("/", response_model=validator.UserOut, status_code=201)
async def create_user(user: validator.UserCreate,
                      db: AsyncSession = Depends(get_db_session)):
    try:
        user = await user_service.create_user(db, user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating user.")


# List all users (Admin only)
@router.get("/", response_model=list[validator.UserOut])
async def get_users(db: AsyncSession = Depends(get_db_session)):
    try:
        return await user_service.get_users(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching users.")


# Update current user details (User only)
@router.put("/me", response_model=validator.UserOut, status_code=200)
async def update_current_user(request: Request, user: validator.UserUpdate,
                              db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        user_id = int(user_data['sub'])
        updated_user = await user_service.update_user(db, user_id, user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating current user.")


# Retrieve current user details (User only)
@router.get("/me", response_model=validator.UserOut)
async def get_current_user(request: Request,
                           db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        user_id = int(user_data['sub'])
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching current user.")


# Get user by ID (Admin and User if self)
@router.get("/{user_id}", response_model=validator.UserOut)
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
@router.put("/{user_id}", response_model=validator.UserOut, status_code=200)
async def update_user(user_id: int, user: validator.UserUpdate,
                      db: AsyncSession = Depends(get_db_session)):
    try:
        updated_user = await user_service.update_user(db, user_id, user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating user.")


# Delete user (Admin only)
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    try:
        await user_service.delete_user(db, user_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting user.")


# List orders for a specific user (Admin)
@router.get("/{user_id}/orders", response_model=list[order_validator.OrderOut])
async def get_user_orders(user_id: int,
                          db: AsyncSession = Depends(get_db_session)):
    try:
        orders = await order_service.get_orders_by_user(db, user_id)
        return orders
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching user orders.")
