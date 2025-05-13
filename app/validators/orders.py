import math
from enum import Enum
from decimal import Decimal
from datetime import datetime
from app.db.models.order import OrderStatusEnum
from pydantic import BaseModel, field_validator, model_validator


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
        from_attributes = True


class OrderCreate(BaseModel):
    total_amount: Decimal

    @field_validator("total_amount")
    @classmethod
    def validate_total_amount(cls, v: Decimal) -> Decimal:
        if not math.isfinite(float(v)):
            raise ValueError("total_amount must be a finite number")
        if v <= 0:
            raise ValueError("total_amount must be greater than zero")
        return v


class OrderUpdate(BaseModel):
    user_id: int | None = None
    order_date: datetime | None = None
    total_amount: Decimal | None = None
    status: OrderStatusEnum | None = None

    @model_validator(mode="after")
    def check_total_amount_if_present(self) -> "OrderUpdate":
        if self.total_amount is not None:
            if not math.isfinite(float(self.total_amount)):
                raise ValueError("total_amount must be a finite number")
            if self.total_amount <= 0:
                raise ValueError("total_amount must be greater than zero")
        return self
