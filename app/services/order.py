from fastapi import HTTPException
from sqlalchemy.future import select
from app.db.models import User, Order
from app.db.models.order import OrderStatusEnum
from app.validators import orders as validator
from sqlalchemy.ext.asyncio import AsyncSession


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_orders_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    return result.scalars().all()


async def create_order(db: AsyncSession, user_id: int, order_data: validator.OrderCreate):
    # Check if user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    # Create new order
    order = Order(
        user_id=user_id,
        total_amount=order_data.total_amount,
    )

    db.add(order)
    await db.flush()  # Auto populate order_id
    return order


async def update_order(db: AsyncSession, order_id: int, order_data: validator.OrderUpdate):
    # Check if order exists
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order fields
    if order_data.user_id is not None:
        # Check if user exists
        user_result = await db.execute(
            select(User).where(User.id == order_data.user_id)
        )
        if not user_result.scalar_one_or_none():
            raise HTTPException(
                status_code=404, detail="Target user not found")
        order.user_id = order_data.user_id

    if order_data.order_date is not None:
        order.order_date = order_data.order_date

    if order_data.total_amount is not None:
        order.total_amount = order_data.total_amount

    if order_data.status is not None:
        # Check if status is valid
        if order_data.status not in [status.value for status in OrderStatusEnum]:
            raise HTTPException(
                status_code=400, detail="Invalid order status provided")
        order.status = order_data.status

    db.add(order)
    await db.flush()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: int):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise ValueError("Order not found")

    await db.delete(order)
    await db.flush()
