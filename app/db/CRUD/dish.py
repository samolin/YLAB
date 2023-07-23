from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.dish import DishCreate
from ..models.dish import Dish


def create_new_dish(dish: DishCreate, db: Session, sub_id: UUID):
    dish_obj = Dish(
        title = dish.title,
        description = dish.description,
        price = dish.price,
        submenu_id = sub_id,
    )
    db.add(dish_obj)
    db.commit()
    db.refresh(dish_obj)
    return dish_obj


def list_dishes(db: Session, sub_id: UUID):
    dishes = db.query(Dish).filter(Dish.submenu_id == sub_id).all()
    return dishes


def get_dish_by_id(db: Session, dish_id: UUID):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return dish


def update_dish_by_id(dish: DishCreate, db: Session, dish_id: UUID):
    existing_dish = db.query(Dish).filter(Dish.id == dish_id)
    existing_dish.update(dish.__dict__)
    db.commit()
    return existing_dish.first()


def delete_dish(db: Session, dish_id: UUID):
    dish = db.query(Dish).filter(Dish.id == dish_id)
    dish.delete()
    db.commit()
    return dish
