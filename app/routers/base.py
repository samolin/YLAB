from fastapi import APIRouter

from . import menu

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(menu.router, prefix='/menus', tags=['menus'])
