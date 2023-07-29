from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.db.CRUD.menu import create_new_menu, list_menu, update_menu_by_id, delete_menu, retrieve_menu
from app.db.CRUD.submenu import create_new_submenu, list_submenus, get_submenu_by_id, update_submenu_by_id, delete_submenu
from app.db.CRUD.dish import create_new_dish, list_dishes, get_dish_by_id, update_dish_by_id, delete_dish
from app.schemas.menu import MenuCreate
from app.schemas.submenu import SubmenuCreate
from app.schemas.dish import DishCreate, DishShow
from app.utils.counter import menu_counter, submenu_counter

router = APIRouter()



@router.post('', status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
   menu = create_new_menu(menu=menu, db=db)
   return menu


@router.get('')
def get_menus(db: Session = Depends(get_db)):
    menus = list_menu(db)
    for menu in menus:
        menu.submenus_count, menu.dishes_count = menu_counter(id=menu.id, db=db)
    return menus


@router.get("/{id}")
def get_menu(id: UUID, db: Session = Depends(get_db)):
    menu = retrieve_menu(id=id, db=db)
    if menu:
        menu.submenus_count, menu.dishes_count = menu_counter(id=id, db=db)
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
            detail=f"menu not found",
        )
    return message


@router.delete('/{id}')
def del_menu(id: UUID, db: Session = Depends(get_db)):
    menu = delete_menu(db=db, id=id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"menu not found",
        )
    return {
        "message": "The menu has been deleted"
        }



@router.post('/{id}/submenus', status_code=201)
def create_submenus(submenu: SubmenuCreate, id: UUID, db: Session = Depends(get_db)):
    menu = create_new_submenu(id=id, db=db, submenu=submenu)
    return menu


@router.get('/{id}/submenus')
def get_submenus(id: UUID, db: Session = Depends(get_db)):
    submenus = list_submenus(id=id, db=db)
    for submenu in submenus:
        submenu.dishes_count = submenu_counter(sub_id=submenu.id, db=db)
    return submenus


@router.get('/{id}/submenus/{sub_id}')
def get_submenu(id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    submenu = get_submenu_by_id(id=id, sub_id=sub_id, db=db)
    if submenu:
        submenu.dishes_count = submenu_counter(sub_id=sub_id, db=db)
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"submenu not found",
        )
    return submenu


@router.patch('/{id}/submenus/{sub_id}')
def update_submenu(id: UUID, sub_id: UUID, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    message = update_submenu_by_id(id=id, sub_id=sub_id, submenu=submenu, db=db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"submenu not found",
        )
    return message


@router.delete('/{id}/submenus/{sub_id}')
def del_submenu(id: UUID, sub_id: UUID, db: Session = Depends(get_db)):
    submenu = delete_submenu(db=db, id=id, sub_id=sub_id)
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"submenu not found",
        )
    return {"msg": "Successfully deleted data"}


@router.post('/{id}/submenus/{sub_id}/dishes', status_code=201, response_model=DishShow)
def create_dish(dish: DishCreate, sub_id: UUID, db: Session = Depends(get_db)):
    dish = create_new_dish(sub_id=sub_id, db=db, dish=dish)
    return dish


@router.get('/{id}/submenus/{sub_id}/dishes')
def get_dishes(sub_id: UUID, db: Session = Depends(get_db)):
    dishes = list_dishes(sub_id=sub_id, db=db)
    return dishes


@router.get('/{id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishShow | None)
def get_dish(dish_id: UUID, db: Session = Depends(get_db)):
    dish = get_dish_by_id(dish_id=dish_id, db=db)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"dish not found",
        )
    return dish


@router.patch('/{id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishShow)
def update_dish(dish: DishCreate, dish_id: UUID, db: Session = Depends(get_db)):
    message = update_dish_by_id(dish_id=dish_id, db=db, dish=dish)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu with id: {dish_id} was not found",
        )
    return message


@router.delete('/{id}/submenus/{sub_id}/dishes/{dish_id}')
def del_dish(id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    dish = delete_dish(db=db, dish_id=dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu with id {dish_id} not found",
        )
    return {"msg": "Successfully deleted data"}
