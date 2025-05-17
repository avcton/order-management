from fastapi import APIRouter


def get_api_router(entity: str) -> APIRouter:
    router = APIRouter(
        prefix=f"/api/{entity}"
    )

    return router
