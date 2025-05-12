from app.db.models import Order
from sqlalchemy.future import select
from fastapi import APIRouter, Depends
from app.validators.orders import OrderOut
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/orders", response_model=list[OrderOut])
async def get_orders(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Order))
    return result.scalars().all()
