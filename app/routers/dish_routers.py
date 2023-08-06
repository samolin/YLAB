from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.db.CRUD.dish import (
    create_new_dish,
    delete_dish,
    get_dish_by_id,
    list_dishes,
    update_dish_by_id,
)
from app.db.database import get_db
from app.schemas.dish_schemas import DishCreate, DishSchema
from app.utils.cache_utils import cache_deleter, id_key_builder

router = APIRouter()


@router.post('/dishes', status_code=201, response_model=DishSchema)
def create_dish(dish: DishCreate, id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    dish = create_new_dish(sub_id=sub_id, db=db, dish=dish)
    cache_deleter()
    return dish


@router.get('/dishes', status_code=200,)
@cache(key_builder=id_key_builder, namespace='dish')
def get_dishes(id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    dishes = list_dishes(sub_id=sub_id, db=db)
    return dishes


@router.get('/dishes/{dish_id}', response_model=DishSchema)
@cache(key_builder=id_key_builder, namespace='dish')
def get_dish(id: UUID, sub_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    dish = get_dish_by_id(dish_id=dish_id, db=db)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    return dish


@router.patch('/dishes/{dish_id}', response_model=DishSchema)
def update_dish(dish: DishCreate, dish_id: UUID, db: Session = Depends(get_db)):
    message = update_dish_by_id(dish_id=dish_id, db=db, dish=dish)
    cache_deleter()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Menu with id: {dish_id} was not found',
        )
    return message


@router.delete('/dishes/{dish_id}')
def del_dish(id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    dish = delete_dish(db=db, dish_id=dish_id)
    cache_deleter()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Menu with id {dish_id} not found',
        )
    return {'msg': 'Successfully deleted data'}
