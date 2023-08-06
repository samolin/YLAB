from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.db.CRUD.submenu import (
    create_new_submenu,
    delete_submenu,
    get_submenu_by_id,
    list_submenus,
    update_submenu_by_id,
)
from app.db.database import get_db
from app.schemas.submenu_schemas import SubmenuCreate
from app.utils.cache_utils import cache_deleter, id_key_builder
from app.utils.counter import submenu_counter

router = APIRouter()


@router.post('/submenus', status_code=201)
def create_submenus(submenu: SubmenuCreate, id: UUID, db: Session = Depends(get_db)):
    menu = create_new_submenu(id=id, db=db, submenu=submenu)
    cache_deleter()
    return menu


@router.get('/submenus')
@cache(key_builder=id_key_builder, namespace='submenu')
def get_submenus(id: UUID, db: Session = Depends(get_db)):
    submenus = list_submenus(id=id, db=db)
    for submenu in submenus:
        submenu.dishes_count = submenu_counter(sub_id=submenu.id, db=db)
    return submenus


@router.get('/submenus/{sub_id}')
@cache(key_builder=id_key_builder, namespace='submenu')
def get_submenu(id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    submenu = get_submenu_by_id(id=id, sub_id=sub_id, db=db)
    if submenu:
        submenu.dishes_count = submenu_counter(sub_id=sub_id, db=db)
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )
    return submenu


@router.patch('/submenus/{sub_id}')
def update_submenu(id: UUID, sub_id: UUID, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    message = update_submenu_by_id(id=id, sub_id=sub_id, submenu=submenu, db=db)
    cache_deleter()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )
    return message


@router.delete('/submenus/{sub_id}')
def del_submenu(id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    submenu = delete_submenu(db=db, id=id, sub_id=sub_id)
    cache_deleter()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )
    return {'msg': 'Successfully deleted data'}
