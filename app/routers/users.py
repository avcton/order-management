from app.db.models import User
from sqlalchemy.future import select
from fastapi import APIRouter, Depends
from app.validators.users import UserOut
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User))
    return result.scalars().all()
