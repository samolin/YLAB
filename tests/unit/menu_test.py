import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from tests.unit.conftest import client
import json


def test_initial_menu():
    response = client.get("api/v1//menus")
    assert response.status_code == 200
    assert response.json() == []


def test_menu_create():
    payload = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = client.post("/api/v1/menus", content=json.dumps(payload))
    assert response.status_code == 201
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']

