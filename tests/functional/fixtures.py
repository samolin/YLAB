import pytest
from sqlalchemy import delete, insert

from app.db.database import async_session_maker
from app.db.models.menu_model import Menu
from app.db.models.submenu_model import Submenu


@pytest.fixture(scope='module')
async def create_menu_fixture():
    async with async_session_maker() as session:
        payload = {
            'title': 'My menu for submenu 1',
            'description': 'My description for submenu 1'
        }
        query = insert(Menu).values(payload).returning(Menu.id)
        res = await session.execute(query)
        await session.commit()
        menu_id = res.scalar_one()
        yield menu_id
        query = delete(Menu).filter(Menu.id == menu_id)
        await session.execute(query)
        await session.commit()


@pytest.fixture(scope='module')
async def create_submenu_fixture():
    async with async_session_maker() as session:
        menu_payload = {
            'title': 'My test menu 1',
            'description': 'My test menu description 1'
        }
        query = insert(Menu).values(menu_payload).returning(Menu.id)
        res = await session.execute(query)
        await session.commit()
        menu_id = res.scalar_one()
        submenu_payload = {
            'title': 'My test submenu 1',
            'description': 'My test submenu description 1',
            'menu_id': f'{str(menu_id)}'
        }
        query = insert(Submenu).values(submenu_payload).returning(Submenu.id)
        res = await session.execute(query)
        await session.commit()
        submenu_id = res.scalar_one()
        yield menu_id, submenu_id
        query = delete(Menu).filter(Menu.id == menu_id)
        await session.execute(query)
        await session.commit()


@pytest.fixture(scope='module')
async def ids():
    keys = {}
    yield keys
