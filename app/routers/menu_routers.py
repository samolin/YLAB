from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.db.CRUD.menu import (
    create_new_menu,
    delete_menu,
    list_menus,
    retrieve_menu,
    update_menu_by_id,
)
from app.db.database import get_db
from app.schemas.menu_schemas import MenuCreate
from app.utils.cache_utils import cache_deleter, id_key_builder
from app.utils.counter import menu_counter

router = APIRouter()


@router.post('', status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    menu = create_new_menu(menu=menu, db=db)
    cache_deleter()
    return menu


@router.get('')
@cache(key_builder=id_key_builder, namespace='menu')
def get_menus(db: Session = Depends(get_db)):
    menus = list_menus(db)
    for menu in menus:
        menu.submenus_count, menu.dishes_count = menu_counter(id=menu.id, db=db)
    return menus


@router.get('/{id}')
@cache(key_builder=id_key_builder, namespace='menu')
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
    cache_deleter()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return message


@router.delete('/{id}')
def del_menu(id: UUID, db: Session = Depends(get_db)):
    menu = delete_menu(db=db, id=id)
    cache_deleter()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return {
        'message': 'The menu has been deleted'
    }
