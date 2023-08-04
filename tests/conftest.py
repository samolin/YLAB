import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database

from app.db.database import engine
from app.main import app

pytest_plugins = ('tests.functional.fixtures')

client = TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def drop_database_fixture():
    yield
    drop_database(engine.url)
