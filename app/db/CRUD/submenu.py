from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.submenu import SubmenuCreate
from ..models.submenu import Submenu


def create_new_submenu(submenu: SubmenuCreate, db: Session, id: UUID):
    submenu_obj = Submenu(
        title = submenu.title,
        description = submenu.description,
        menu_id = id,
    )
    db.add(submenu_obj)
    db.commit()
    db.refresh(submenu_obj)
    return submenu_obj
