from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.schemas.menu_schemas import MenuSchema

from ..database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: str = Column(String(50), nullable=False, unique=True)
    description: str = Column(String(256), nullable=True)
    submenus = relationship('Submenu', back_populates='menu', cascade='delete')

    def to_read_model(self) -> MenuSchema:
        return MenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus=self.submenus,
        )
