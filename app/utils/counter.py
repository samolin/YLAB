from sqlalchemy.orm import Session

from app.db.models.dish_model import Dish
from app.db.models.submenu_model import Submenu


def menu_counter(id, db: Session):
    sub_count = 0
    dish_counter = 0
    submenus = db.query(Submenu).filter(Submenu.menu_id == id).all()
    sub_count = len(submenus)
    for submenu in submenus:
        dishlen = len(submenu.dishes)
        dish_counter += dishlen
    return sub_count, dish_counter


def submenu_counter(sub_id, db: Session):
    dish_counter = 0
    dish_counter = db.query(Dish).filter(Dish.submenu_id == sub_id).count()
    return dish_counter
