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




client = TestClient(app)