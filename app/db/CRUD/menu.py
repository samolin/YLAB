from uuid import UUID

from sqlalchemy.orm import Session

from app.schemas.menu_schemas import MenuCreate

from ..models.menu_model import Menu


def create_new_menu(menu: MenuCreate, db: Session) -> Menu:
    menu_obj = Menu(
        title=menu.title,
        description=menu.description,
    )
    db.add(menu_obj)
    db.commit()
    db.refresh(menu_obj)
    return menu_obj


def list_menu(db: Session):
    menus = db.query(Menu).all()
    return menus


def retrieve_menu(id: UUID, db: Session):
    item = db.query(Menu).filter(Menu.id == id).first()
    return item


def update_menu_by_id(id: UUID, db: Session, menu: MenuCreate):
    existing_menu = db.query(Menu).filter(Menu.id == id)
    if not existing_menu.first():
        return 0
    existing_menu.update(menu.__dict__)
    db.commit()
    return existing_menu.first()


def delete_menu(db: Session, id: UUID):
    menu = db.query(Menu).filter(Menu.id == id)
    if not menu.first():
        return 0
    menu.delete()
    db.commit()
    return 1
