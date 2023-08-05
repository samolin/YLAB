from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Submenu(Base):
    __tablename__ = 'submenu'

    id: Column[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Column[str] = Column(String(50), nullable=False, unique=True)
    description: Column[str] = Column(String(256), nullable=True)
    menu_id: Column[UUID] = Column(UUID, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='delete')
