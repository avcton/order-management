import uvicorn
from fastapi import FastAPI
from app.config.settings import settings
from app.routers import auth, users, orders
from app.middlewares.auth import TokenAuthMiddleware


app = FastAPI()

# Add authentication middleware
app.add_middleware(TokenAuthMiddleware,
                   token_url="/api/auth/login",
                   exclude_paths=[
                       "/docs",
                       "/openapi.json",
                       "/api/auth/refresh"])

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
