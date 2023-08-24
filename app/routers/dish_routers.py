from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache

from app.repositories.dish_repository import DishRepository
from app.schemas.dish_schemas import DishCreate, DishSchema
from app.utils.cache_utils import cache_deleter, id_key_builder

router = APIRouter()


@router.post('/dishes', status_code=201, response_model=DishSchema)
async def create_dish(dish: DishCreate, id: UUID, sub_id: UUID, request: Request):
    dish.__setattr__('submenu_id', sub_id)
    dish = await DishRepository().add_new(dish.model_dump())
    await cache_deleter(path=request.url.path)
    return dish


@router.get('/dishes', status_code=200, response_model=list[DishSchema])
@cache(key_builder=id_key_builder, namespace='dish')
async def get_dishes(id: UUID, sub_id: UUID):
    dishes = await DishRepository().get_all(submenu_id=sub_id)
    return dishes


@router.get('/dishes/{dish_id}', status_code=200, response_model=DishSchema)
@cache(key_builder=id_key_builder, namespace='dish')
async def get_dish(id: UUID, sub_id: UUID, dish_id: UUID):
    dish = await DishRepository().get_one(dish_id=dish_id)
    return dish


@router.patch('/dishes/{dish_id}', status_code=200, response_model=DishSchema)
async def update_dish(dish: DishCreate, id: UUID, sub_id: UUID, dish_id: UUID, request: Request):
    dish.__setattr__('submenu_id', sub_id)
    dish = await DishRepository().patch_one(dish.model_dump(), dish_id=dish_id)
    await cache_deleter(path=request.url.path)
    return dish


@router.delete('/dishes/{dish_id}', status_code=200)
async def del_dish(id: UUID, sub_id: UUID, dish_id: UUID, request: Request):
    await DishRepository().del_one(dish_id=dish_id)
    await cache_deleter(path=request.url.path)
    return {'msg': 'Successfully deleted data'}
