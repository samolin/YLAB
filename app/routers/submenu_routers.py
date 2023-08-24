from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache

from app.repositories.submenu_repository import SubmenuRepository
from app.schemas.submenu_schemas import SubmenuCreate, SubmenuSchema, SubmenuUpdate
from app.utils.cache_utils import cache_deleter, id_key_builder

router = APIRouter()


@router.post('/submenus', status_code=201, response_model=SubmenuUpdate)
async def create_submenu(submenu: SubmenuCreate, id: UUID, request: Request):
    submenu.__setattr__('menu_id', id)
    submenu = await SubmenuRepository().add_new(submenu.model_dump())
    await cache_deleter(path=request.url.path)
    return submenu


@router.get('/submenus', status_code=200, response_model=list[SubmenuSchema])
@cache(key_builder=id_key_builder, namespace='submenu')
async def get_submenus(id: UUID):
    submenus = await SubmenuRepository().get_all(menu_id=id)
    return submenus


@router.get('/submenus/{sub_id}', status_code=200, response_model=SubmenuSchema)
@cache(key_builder=id_key_builder, namespace='submenu')
async def get_submenu(id: UUID, sub_id: UUID):
    submenu = await SubmenuRepository().get_one(submenu_id=sub_id)
    return submenu


@router.patch('/submenus/{sub_id}', status_code=200, response_model=SubmenuUpdate)
async def update_submenu(id: UUID, sub_id: UUID, submenu: SubmenuCreate, request: Request):
    submenu.__setattr__('menu_id', id)
    submenu = await SubmenuRepository().patch_one(submenu.model_dump(), submenu_id=sub_id)
    await cache_deleter(path=request.url.path)
    return submenu


@router.delete('/submenus/{sub_id}', status_code=200)
async def del_submenu(id: UUID, sub_id: UUID, request: Request):
    await SubmenuRepository().del_one(submenu_id=sub_id)
    await cache_deleter(path=request.url.path)
    return {'msg': 'Successfully deleted data'}
