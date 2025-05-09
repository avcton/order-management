from pydantic import BaseModel
from app.db.models.order import OrderStatusEnum


class OrderStatusModel(BaseModel):
    status: OrderStatusEnum = OrderStatusEnum.pending
