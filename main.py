import uvicorn
from fastapi import FastAPI
from app.config.settings import settings
from app.routers import auth, users, orders


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
