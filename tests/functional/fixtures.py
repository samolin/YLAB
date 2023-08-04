import pytest

from app.db.database import get_db
from app.db.models.menu_model import Menu
from app.db.models.submenu_model import Submenu

db = next(get_db())


@pytest.fixture(scope='module')
def create_menu_fixture():
    menu_obj = Menu(
        title='My menu for submenu 1',
        description='My description for submenu 1'
    )
    db.add(menu_obj)
    db.commit()
    menu = db.query(Menu).filter(Menu.id == menu_obj.id).first()
    yield menu.id
    menu = db.query(Menu).filter(Menu.id == menu_obj.id)
    menu.delete()
    db.commit()


@pytest.fixture(scope='module')
def create_submenu_fixture():
    menu_obj = Menu(
        title='My menu for submenu 1',
        description='My description for submenu 1'
    )
    db.add(menu_obj)
    db.commit()
    menu = db.query(Menu).filter(Menu.id == menu_obj.id).first()
    submenu_obj = Submenu(
        title='My menu for submenu 1',
        description='My description for submenu 1',
        menu_id=str(menu.id)
    )
    db.add(submenu_obj)
    db.commit()
    submenu = db.query(Submenu).filter(Submenu.id == submenu_obj.id).first()
    yield menu.id, submenu.id
    menu = db.query(Menu).filter(Menu.id == menu_obj.id)
    menu.delete()
    db.commit()


@pytest.fixture(scope='module')
def ids():
    keys = {}
    yield keys
