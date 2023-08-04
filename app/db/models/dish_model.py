from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: str = Column(String(50), nullable=False, unique=True)
    description: str = Column(String(256), nullable=True)
    price: float = Column(Numeric(10, 2), nullable=False)
    submenu_id: UUID = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship('Submenu', back_populates='dishes')
