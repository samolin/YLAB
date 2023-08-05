from fastapi import APIRouter

from . import dish, menu, submenu

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(menu.router, prefix='/menus', tags=['menus'])
api_router.include_router(submenu.router, prefix='/menus/{id}', tags=['submenus'])
api_router.include_router(dish.router, prefix='/menus/{id}/submenus/{sub_id}', tags=['dishes'])
