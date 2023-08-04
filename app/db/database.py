from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
