from app.validators import orders as validator
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.validators.auth import AccessTokenData
from app.services import order as order_service
from app.middlewares.router import get_api_router
from fastapi import Depends, HTTPException, Request
from app.middlewares.privileges import has_privilege, has_any_privilege

router = get_api_router("orders")


# List all orders (Admin Only)
@router.get("/", response_model=list[validator.OrderOut])
async def get_orders(request: Request, db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'l_a_o')

        return await order_service.get_orders(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching orders.")


# List orders placed by current user (User only)
@router.get("/me", response_model=list[validator.OrderOut])
async def get_orders_by_user(request: Request,
                             db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'l_o_o')

        user_id = int(user_data['sub'])
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
@router.get("/{order_id}", response_model=validator.OrderOut)
async def get_order_by_id(request: Request, order_id: int,
                          db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['v_a_o', 'v_o_o'])

        order = await order_service.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if 'v_a_o' not in user_data['privileges']:
            # Check if the order belongs to the current user
            user_id = int(user_data['sub'])
            if order.user_id != user_id:
                raise HTTPException(status_code=403, detail="Access denied")

        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching order.")


# Create new order for current user (Admin and User)
@router.post("/", response_model=validator.OrderOut, status_code=201)
async def create_order(request: Request, order: validator.OrderCreate,
                       db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_privilege(user_data, 'c_n_o')

        user_id = int(user_data['sub'])
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
@router.put("/{order_id}", response_model=validator.OrderOut)
async def update_order(request: Request, order_id: int,
                       order_data: validator.OrderUpdate,
                       db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['u_a_o', 'u_o_o'])

        # Restrict access to self orders if the user can't update all orders
        if 'u_a_o' not in user_data['privileges']:
            user_id = int(user_data['sub'])
            user_orders = await order_service.get_orders_by_user(db, user_id)
            if order_id not in [order.id for order in user_orders]:
                raise HTTPException(status_code=403, detail="Access denied")

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
@router.delete("/{order_id}", status_code=204)
async def delete_order(request: Request, order_id: int,
                       db: AsyncSession = Depends(get_db_session)):
    try:
        user_data: AccessTokenData = request.state.user
        # Check if the user has the required privilege
        has_any_privilege(user_data, ['d_a_o', 'd_o_o'])

        # Restrict access to self orders if the user can't delete all orders
        if 'd_a_o' not in user_data['privileges']:
            user_id = int(user_data['sub'])
            user_orders = await order_service.get_orders_by_user(db, user_id)
            if order_id not in [order.id for order in user_orders]:
                raise HTTPException(status_code=403, detail="Access denied")

        await order_service.delete_order(db, order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting order.")
