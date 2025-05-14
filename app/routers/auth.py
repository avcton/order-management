from jose import jwt
import app.validators.auth as validator
from app.config.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import authenticate_user, token_refresh


router = APIRouter(prefix="/auth")


@router.post("/login", response_model=validator.AccessTokenResponse, status_code=201)
async def login(
    data: validator.LoginRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        token = await authenticate_user(db, data)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred during authentication.")


@router.post("/refresh", response_model=validator.RefreshResponse)
async def refresh_token(refresh_request: validator.RefreshRequest,
                        db: AsyncSession = Depends(get_db_session)):
    try:
        token = await token_refresh(db, refresh_request)
        return token
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred during token refresh.")
