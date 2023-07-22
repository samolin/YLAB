from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..base_class import Base


class Menu(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    submenus = relationship("Submenu", back_populates="menu", cascade="delete")
    # submenus_count = 
    # dishes_count = 
    