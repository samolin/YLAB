from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from ..base_class import Base

class Dish(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    price = Column(Numeric(10, 2), nullable=False) 
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship('Submenu', back_populates="dishes")
