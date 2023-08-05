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
from app.schemas.dish_schemas import DishCreate, DishShow

router = APIRouter()


@router.post('/dishes', status_code=201, response_model=DishShow)
def create_dish(dish: DishCreate, sub_id: UUID, db: Session = Depends(get_db)):
    dish = create_new_dish(sub_id=sub_id, db=db, dish=dish)
    return dish


@router.get('/dishes')
@cache(expire=60)
def get_dishes(sub_id: UUID, db: Session = Depends(get_db)):
    dishes = list_dishes(sub_id=sub_id, db=db)
    return dishes


@router.get('/dishes/{dish_id}', response_model=DishShow | None)
@cache(expire=60)
def get_dish(dish_id: UUID, db: Session = Depends(get_db)):
    dish = get_dish_by_id(dish_id=dish_id, db=db)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    return dish


@router.patch('/dishes/{dish_id}', response_model=DishShow)
def update_dish(dish: DishCreate, dish_id: UUID, db: Session = Depends(get_db)):
    message = update_dish_by_id(dish_id=dish_id, db=db, dish=dish)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Menu with id: {dish_id} was not found',
        )
    return message


@router.delete('/dishes/{dish_id}')
def del_dish(id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    dish = delete_dish(db=db, dish_id=dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Menu with id {dish_id} not found',
        )
    return {'msg': 'Successfully deleted data'}
