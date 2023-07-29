import pytest

from app.db.models.menu import Menu
from app.db.database import get_db


db = next(get_db())

@pytest.fixture(scope="function")
def create_menu_fixture():
    menu_obj = Menu(
        title = 'title1',
        description = 'description1',
    )
    db.add(menu_obj)
    db.commit()
    yield
    menu = db.query(Menu).filter(Menu.id==menu_obj.id)
    menu.delete()
    db.commit()


@pytest.fixture(scope='module')
def ids():
    keys = {}
    yield keys
