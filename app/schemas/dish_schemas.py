from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class DishSchema(BaseModel):
    id: UUID
    title: str
    description: str
    price: float

    @field_validator('price')
    @classmethod
    def validate_price(cls, value):
        value = f'{value:.2f}'
        return str(value)


class DishCreate(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)
