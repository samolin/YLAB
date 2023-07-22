from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..base_class import Base


class Submenu(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    menu = relationship('Menu', back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="delete")
    # dishes_count = 