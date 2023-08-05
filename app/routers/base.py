from fastapi import APIRouter

from . import menu, submenu

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(menu.router, prefix='/menus', tags=['menus'])
api_router.include_router(submenu.router, prefix='/menus/{id}', tags=['submenus'])
