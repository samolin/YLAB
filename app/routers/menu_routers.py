from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache

from app.celery.tasks import db_sync
from app.repositories.menu_repository import MenuRepository
from app.schemas.menu_schemas import MenuCreate, MenuSchema, MenuUpdate
from app.utils.cache_utils import cache_deleter, id_key_builder
from app.utils.excel_reader import convert_excel_to_json

router = APIRouter()


@router.get('/all_menu', status_code=200)
async def get_all_menu(request: Request):
    everything = await MenuRepository().get_everything()
    admin_f = await convert_excel_to_json()
    print(admin_f)
    task = db_sync.delay()
    print(task)
    return everything


@router.post('', status_code=201, response_model=MenuUpdate)
async def create_menu(menu: MenuCreate, request: Request):
    menu = await MenuRepository().add_new(menu.model_dump())
    await cache_deleter(path=request.url.path)
    return menu


@router.get('', status_code=200, response_model=list[MenuSchema])
@cache(key_builder=id_key_builder, namespace='menu')
async def get_menus():
    menus = await MenuRepository().get_all()
    return menus


@router.get('/{id}', status_code=200, response_model=MenuSchema)
@cache(key_builder=id_key_builder, namespace='menu')
async def get_menu(id: UUID):
    menu = await MenuRepository().get_one(id=id)
    return menu


@router.patch('/{id}', status_code=200, response_model=MenuUpdate)
async def update_menu(id: UUID, menu: MenuCreate, request: Request):
    menu = await MenuRepository().patch_one(id, menu.model_dump())
    await cache_deleter(path=request.url.path)
    return menu


@router.delete('/{id}', status_code=200)
async def del_menu(id: UUID, request: Request):
    await MenuRepository().del_one(id=id)
    await cache_deleter(path=request.url.path)
    return {
        'message': 'The menu has been deleted'
    }
