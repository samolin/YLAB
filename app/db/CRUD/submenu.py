from uuid import UUID

from sqlalchemy.orm import Session

from app.schemas.submenu_schemas import SubmenuCreate

from ..models.submenu_model import Submenu


def create_new_submenu(submenu: SubmenuCreate, db: Session, id: UUID) -> Submenu:
    submenu_obj = Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=id,
    )
    db.add(submenu_obj)
    db.commit()
    db.refresh(submenu_obj)
    return submenu_obj


def list_submenus(db: Session, id: UUID) -> list[Submenu]:
    submenus = db.query(Submenu).filter(Submenu.menu_id == id).all()
    return submenus


def get_submenu_by_id(db: Session, id: UUID, sub_id: UUID) -> Submenu:
    submenu = db.query(Submenu).filter(Submenu.id == sub_id).first()
    return submenu


def update_submenu_by_id(id: UUID, sub_id: UUID, db: Session, submenu: SubmenuCreate) -> Submenu:
    existing_submenu = db.query(Submenu).filter(Submenu.id == sub_id)
    existing_submenu.update(submenu.__dict__)
    db.commit()
    return existing_submenu.first()


def delete_submenu(db: Session, id: UUID, sub_id: UUID) -> int:
    submenu = db.query(Submenu).filter(Submenu.id == sub_id)
    if not submenu.first():
        return 0
    submenu.delete()
    db.commit()
    return 1
