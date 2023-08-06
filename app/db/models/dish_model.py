from uuid import uuid4

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    submenu_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu: Mapped[list['Submenu']] = relationship('Submenu', back_populates='dishes')
