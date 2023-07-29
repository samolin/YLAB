from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing import Generator
from sqlalchemy.pool import StaticPool
import pytest

from app.db.base import Base
from app.db.database import engine
from app.core.config import settings
from app.main import app
from app.db.models.menu import Menu
from app.db.database import get_db


client = TestClient(app)

db = next(get_db())


@pytest.fixture(scope='session', autouse=True)
def drop_database_fixture():
    yield
    drop_database(engine.url)


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
