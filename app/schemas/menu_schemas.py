from uuid import UUID

from pydantic import BaseModel


class MenuSchema(BaseModel):
    id: UUID
    title: str
    description: str


class MenuCreate(BaseModel):
    title: str
    description: str
