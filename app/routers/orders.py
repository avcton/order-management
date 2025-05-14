from app.validators.auth import AccessTokenData
from app.validators import orders as validator
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import order as order_service
from app.middlewares.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


# List all orders (Admin Only)
@router.get("/orders", response_model=list[validator.OrderOut])
async def get_orders(db: AsyncSession = Depends(get_db_session)):
    try:
        return await order_service.get_orders(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching orders.")


# List orders placed by current user (User only)
@router.get("/orders/me", response_model=list[validator.OrderOut])
async def get_orders_by_user(current_user: AccessTokenData = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = int(current_user['sub'])
        orders = await order_service.get_orders_by_user(db, user_id)
        return orders
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching orders.")


# Retrieve order details by ID (Admin Only)
@router.get("/orders/{order_id}", response_model=validator.OrderOut)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db_session)):
    try:
        user = await order_service.get_order_by_id(db, order_id)
        if not user:
            raise HTTPException(status_code=404, detail="Order not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching order.")


# Create new order current user (User only)
@router.post("/orders", response_model=validator.OrderOut, status_code=201)
async def create_order(order: validator.OrderCreate,
                       current_user: AccessTokenData = Depends(
                           get_current_user),
                       db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = int(current_user['sub'])
        order = await order_service.create_order(db, user_id, order)
        return order
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating order.")


# Update order by ID (Admin and User if self order)
@router.put("/orders/{order_id}", response_model=validator.OrderOut)
async def update_order(order_id: int,
                       order_data: validator.OrderUpdate,
                       db: AsyncSession = Depends(get_db_session)):
    try:
        order = await order_service.update_order(db, order_id, order_data)
        return order
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating order.")


# Delete order by ID (Admin and User if self order)
@router.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: int,
                       db: AsyncSession = Depends(get_db_session)):
    try:
        await order_service.delete_order(db, order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting order.")
