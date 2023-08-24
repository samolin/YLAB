from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.menu_schemas import MenuSchema

from ..database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    submenus: Mapped[list['Submenu']] = relationship('Submenu', back_populates='menu', cascade='delete')

    def to_read_model(self, submenus_count: int | None = None, dishes_count: int | None = None) -> MenuSchema:
        return MenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )
