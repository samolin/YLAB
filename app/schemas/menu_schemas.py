from uuid import UUID

from pydantic import BaseModel, field_validator


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdate(MenuCreate):
    id: UUID


class MenuSchema(MenuUpdate):
    submenus_count: int | None = None
    dishes_count: int | None = None


class DishEverithing(BaseModel):
    id: UUID
    title: str
    description: str
    price: float

    @field_validator('price')
    @classmethod
    def validate_price(cls, value):
        value = f'{value:.2f}'
        return str(value)


class SubmenuEverithing(BaseModel):
    id: UUID
    title: str
    description: str
    dishes: list[DishEverithing]


class MenuEverything(BaseModel):
    id: UUID
    title: str
    description: str
    submenus: list[SubmenuEverithing]

    class Confing:
        orm_mode = True
