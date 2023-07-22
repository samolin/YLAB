from sqlalchemy.orm import Session

from ..models.menu import Menu


def list_menu(db: Session):
    menus = db.query(Menu).all()
    return menus


def delete_menu(db: Session, id: int):
    menu = db.query(Menu).filter(Menu.id==id)
    if not menu.first():
        return 0
    menu.delete()
    db.commit()
    return 1