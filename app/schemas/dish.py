from pydantic import BaseModel, field_validator, Field
from uuid import UUID


class DishCreate(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)


class DishShow(BaseModel):
    id: UUID
    title: str
    description: str
    price: float


    @field_validator('price')
    @classmethod
    def validate_price(cls, value):
        value = '{0:.2f}'.format(value)
        return str(value)
