import pytest

from app.db.models.menu import Menu
from app.db.database import get_db


db = next(get_db())

@pytest.fixture(scope="module")
def create_menu_fixture():
    menu_obj = Menu(
        title = 'My menu for submenu 1',
        description = 'My description for submenu 1'
    )
    db.add(menu_obj)
    db.commit()
    menu = db.query(Menu).filter(Menu.id==menu_obj.id).first()
    yield menu.id
    menu = db.query(Menu).filter(Menu.id==menu_obj.id)
    menu.delete()
    db.commit()


@pytest.fixture(scope='module')
def ids():
    keys = {}
    yield keys
