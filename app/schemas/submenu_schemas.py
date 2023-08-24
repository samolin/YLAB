from uuid import UUID

from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    title: str
    description: str
    menu_id: UUID


class SubmenuUpdate(SubmenuCreate):
    id: UUID


class SubmenuSchema(SubmenuUpdate):
    dishes_count: int | None = None
