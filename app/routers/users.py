from app.services import user as user_service
from app.validators import users as validator
from app.config.database import get_db_session
from app.validators.auth import AccessTokenData
from app.services import order as order_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.router import get_api_router
from fastapi import Depends, HTTPException, Request
from app.validators import orders as order_validator
from app.middlewares.privileges import has_privilege, has_any_privilege

router = get_api_router("users")


# Create new user (Admin only)
@router.post("/", response_model=validator.UserOut, status_code=201)
async def create_user(request: Request, user: validator.UserCreate,
                      db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'c_n_u')

        user = await user_service.create_user(db, user)
        return user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating user.")


# List all users (Admin only)
@router.get("/", response_model=list[validator.UserOut])
async def get_users(request: Request, db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'l_a_u')

        return await user_service.get_users(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching users.")


# Update current user details (User only)
@router.put("/me", response_model=validator.UserOut, status_code=200)
async def update_current_user(request: Request, user: validator.UserUpdate,
                              db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'u_o_d')

        # Allow user to update their own role only if they are an admin
        existing_role = user_data['role']
        if user.role and existing_role != 'admin':
            raise HTTPException(
                status_code=403, detail="Only admins can change roles")

        user_id = int(user_data['sub'])
        updated_user = await user_service.update_user(db, user_id, user)
        return updated_user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred while updating current user.")


# Retrieve current user details (User only)
@router.get("/me", response_model=validator.UserOut)
async def get_current_user(request: Request,
                           db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'v_o_d')

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
async def get_user_by_id(request: Request, user_id: int,
                         db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['v_a_u', 'v_o_d'])

        # Restrict access to self only if the user can't view all users
        if 'v_a_u' not in user_data['privileges'] and \
                user_data['sub'] != str(user_id):
            raise HTTPException(status_code=403, detail="Access denied")

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
async def update_user(request: Request, user_id: int, user: validator.UserUpdate,
                      db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['u_a_u', 'u_o_d'])

        # Restrict access to self only if the user can't update all users
        if 'u_a_u' not in user_data['privileges'] and \
                user_data['sub'] != str(user_id):
            raise HTTPException(status_code=403, detail="Access denied")

        existing_role = user_data['role']
        # Allow user to update their own role only if they are an admin
        if user.role and existing_role != 'admin':
            raise HTTPException(
                status_code=403, detail="Only admins can change roles")

        updated_user = await user_service.update_user(db, user_id, user)
        return updated_user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating user.")


# Delete user (Admin only)
@router.delete("/{user_id}", status_code=204)
async def delete_user(request: Request, user_id: int,
                      db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'd_a_u')

        await user_service.delete_user(db, user_id)
        return
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting user.")


# List orders for a specific user (Admin and User if self)
@router.get("/{user_id}/orders", response_model=list[order_validator.OrderOut])
async def get_user_orders(request: Request, user_id: int,
                          db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['l_a_o', 'l_o_o'])

        # Restrict access to self only if the user can't view all orders
        if 'l_a_o' not in user_data['privileges'] and \
                user_data['sub'] != str(user_id):
            raise HTTPException(status_code=403, detail="Access denied")

        orders = await order_service.get_orders_by_user(db, user_id)
        return orders
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching user orders.")
