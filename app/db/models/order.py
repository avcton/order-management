from enum import Enum
from sqlalchemy.sql import func
from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric


class OrderStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Numeric(10, 2), nullable=False, comment=">=0")
    status = Column(SQLAlchemyEnum(OrderStatusEnum, name="statuses"),
                    nullable=False, default=OrderStatusEnum.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
