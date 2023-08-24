from uuid import uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.submenu_schemas import SubmenuSchema

from ..database import Base


class Submenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    menu_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    menu: Mapped[list['Menu']] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu', cascade='delete')

    def to_read_model(self, dishes_count: int | None = None) -> SubmenuSchema:
        return SubmenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            dishes_count=dishes_count,
            menu_id=self.menu_id,
        )
