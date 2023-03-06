from fastapi import APIRouter

from .endpoints import games,users 

api_router = APIRouter()
api_router.include_router(games.router,prefix='/games',tags=['Games'])
api_router.include_router(users.router,prefix="/users",tags=["Users"])
