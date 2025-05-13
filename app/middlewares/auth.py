from jose import jwt
from app.validators.auth import TokenData
from fastapi import Depends, HTTPException
from app.middlewares.jwt import decode_jwt_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload: TokenData = decode_jwt_token(token)
        return payload
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while decoding the token")
