from enum import Enum
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from app.db.models.order import OrderStatusEnum


class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderOut(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: Decimal
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime

    class config:
        orm_mode = True
