from app.config.database import get_db_session
from app.services.auth import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.validators.auth import LoginRequest, Token
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.post("/auth/login", response_model=Token, status_code=201)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        token = await authenticate_user(db, data)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred during authentication.")
