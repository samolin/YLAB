from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.CRUD.menus import list_menu, delete_menu

router = APIRouter()


@router.get('')
def get_menus(db: Session = Depends(get_db)):
    menus = list_menu(db)
    return menus


@router.delete('/{id}/')
def del_menu(id: int, db: Session = Depends(get_db)):
    menu = delete_menu(db=db, id=id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu with id {id} not found",
        )
    return {"msg": "Successfully deleted data"}
