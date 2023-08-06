from uuid import UUID

from pydantic import BaseModel


class SubmenuSchema(BaseModel):
    id: UUID
    title: str
    description: str
    menu_id: UUID


class SubmenuCreate(BaseModel):
    title: str
    description: str
