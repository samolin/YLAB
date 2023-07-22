from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..base_class import Base


class Menu(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    submenus = relationship("Submenu", back_populates="menu", cascade="delete")
    # submenus_count = 
    # dishes_count = 
    