from uuid import UUID

from pydantic import BaseModel


class MenuSchema(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int | None = None
    dishes_count: int | None = None


class MenuCreate(BaseModel):
    title: str
    description: str
