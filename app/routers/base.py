from fastapi import APIRouter

from . import dish_routers, menu_routers, submenu_routers

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(menu_routers.router, prefix='/menus', tags=['menus'])
api_router.include_router(submenu_routers.router, prefix='/menus/{id}', tags=['submenus'])
api_router.include_router(dish_routers.router, prefix='/menus/{id}/submenus/{sub_id}', tags=['dishes'])
