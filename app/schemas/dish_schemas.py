from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class DishCreate(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)
    submenu_id: UUID


class DishSchema(DishCreate):
    id: UUID
    price: float

    @field_validator('price')
    @classmethod
    def validate_price(cls, value):
        value = f'{value:.2f}'
        return str(value)
