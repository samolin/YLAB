from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.db.CRUD.menu import (
    create_new_menu,
    delete_menu,
    list_menu,
    retrieve_menu,
    update_menu_by_id,
)
from app.db.database import get_db
from app.schemas.menu_schemas import MenuCreate
from app.utils.counter import menu_counter

router = APIRouter()


@router.post('', status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    menu = create_new_menu(menu=menu, db=db)
    return menu


@router.get('')
@cache(expire=60)
def get_menus(db: Session = Depends(get_db)):
    menus = list_menu(db)
    for menu in menus:
        menu.submenus_count, menu.dishes_count = menu_counter(id=menu.id, db=db)
    return menus


@router.get('/{id}')
@cache(expire=60)
def get_menu(id: UUID, db: Session = Depends(get_db)):
    menu = retrieve_menu(id=id, db=db)
    if menu:
        menu.submenus_count, menu.dishes_count = menu_counter(id=id, db=db)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return menu


@router.patch('/{id}')
def update_menu(
    id: UUID,
    menu: MenuCreate,
    db: Session = Depends(get_db),
):
    message = update_menu_by_id(id=id, menu=menu, db=db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return message


@router.delete('/{id}')
def del_menu(id: UUID, db: Session = Depends(get_db)):
    menu = delete_menu(db=db, id=id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return {
        'message': 'The menu has been deleted'
    }


# @router.post('/{id}/submenus/{sub_id}/dishes', status_code=201, response_model=DishShow)
# def create_dish(dish: DishCreate, sub_id: UUID, db: Session = Depends(get_db)):
#     dish = create_new_dish(sub_id=sub_id, db=db, dish=dish)
#     return dish


# @router.get('/{id}/submenus/{sub_id}/dishes')
# @cache(expire=60)
# def get_dishes(sub_id: UUID, db: Session = Depends(get_db)):
#     dishes = list_dishes(sub_id=sub_id, db=db)
#     return dishes


# @router.get('/{id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishShow | None)
# @cache(expire=60)
# def get_dish(dish_id: UUID, db: Session = Depends(get_db)):
#     dish = get_dish_by_id(dish_id=dish_id, db=db)
#     if not dish:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='dish not found',
#         )
#     return dish


# @router.patch('/{id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishShow)
# def update_dish(dish: DishCreate, dish_id: UUID, db: Session = Depends(get_db)):
#     message = update_dish_by_id(dish_id=dish_id, db=db, dish=dish)
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'Menu with id: {dish_id} was not found',
#         )
#     return message


# @router.delete('/{id}/submenus/{sub_id}/dishes/{dish_id}')
# def del_dish(id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
#     dish = delete_dish(db=db, dish_id=dish_id)
#     if not dish:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'Menu with id {dish_id} not found',
#         )
#     return {'msg': 'Successfully deleted data'}
