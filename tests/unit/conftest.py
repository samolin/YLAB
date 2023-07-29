from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing import Generator
from sqlalchemy.pool import StaticPool
import pytest

from app.db.base import Base
from app.db.database import get_db
from app.core.config import settings
from app.main import app


engine = create_engine(settings.DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        drop_database(engine.url)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)