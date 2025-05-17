from jose import jwt
from fastapi import Depends, HTTPException
from app.validators.auth import AccessTokenData
from app.services.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> AccessTokenData:
    try:
        payload: AccessTokenData = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid access token")
        return payload
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while decoding the token")
