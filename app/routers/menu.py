from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.db.CRUD.menu import create_new_menu, list_menu, update_menu_by_id, delete_menu, retrieve_menu
from app.db.CRUD.submenu import create_new_submenu
from app.schemas.menu import MenuCreate
from app.schemas.submenu import SubmenuCreate

router = APIRouter()



@router.post('', status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
   menu = create_new_menu(menu=menu, db=db)
   return menu


@router.get('')
def get_menus(db: Session = Depends(get_db)):
    menus = list_menu(db)
    return menus


@router.get("/{id}")
def get_menu(id: UUID, db: Session = Depends(get_db)):
    menu = retrieve_menu(id=id, db=db)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"menu not found",
        )
    return menu


@router.patch("/{id}")
def update_menu(
    id: UUID,
    menu: MenuCreate,
    db: Session = Depends(get_db),
):
    message = update_menu_by_id(id=id, menu=menu, db=db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu with id: {id} was not found",
        )
    return message


@router.delete('/{id}')
def del_menu(id: UUID, db: Session = Depends(get_db)):
    menu = delete_menu(db=db, id=id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu with id {id} not found",
        )
    return {"msg": "Successfully deleted data"}



@router.post('/{id}/submenus', status_code=201)
def create_submenus(submenu: SubmenuCreate, id: UUID, db: Session = Depends(get_db)):
    menu = create_new_submenu(id=id, db=db, submenu=submenu)
    return menu
