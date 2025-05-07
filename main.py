from app.config.settings import settings
from app.routers import users
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(users.router)


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
