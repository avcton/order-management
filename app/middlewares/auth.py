from jose import jwt
from fastapi import Request
from app.validators.auth import TokenType
from fastapi.responses import JSONResponse
from app.validators.auth import AccessTokenData
from app.services.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token_url, exclude_paths: list[str] = []):
        super().__init__(app)
        self.token_url = token_url
        self.exclude_paths = exclude_paths
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.token_url)

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for these paths
        if request.url.path in [self.token_url, *self.exclude_paths]:
            return await call_next(request)

        authorization: str = request.headers.get("authorization")
        if not authorization or not authorization.startswith(TokenType.BEARER.value):
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

        # Extract token from authorization header
        token = authorization.split(' ')[1].strip()

        try:
            payload: AccessTokenData = decode_access_token(token)
            # Attach user info to request state for use in route handlers
            request.state.user: AccessTokenData = payload

        except jwt.JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
        except Exception as e:
            return JSONResponse(status_code=500,
                                content={"detail": "An error occurred while decoding the token"})

        return await call_next(request)
