from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ..base_class import Base

class Dish(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    price = Column(Numeric(10, 2), nullable=False) 
    submenu_id = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship('Submenu', back_populates="dishes")
