from sqlalchemy.sql import func
from app.config.database import Base
from sqlalchemy.orm import relationship
from app.validators.orders import OrderStatus
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Numeric(10, 2), nullable=False, comment=">=0")
    status = Column(SQLAlchemyEnum(OrderStatus, name="statuses",
                                   values_callable=lambda x: [e.value for e in x]),
                    nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
