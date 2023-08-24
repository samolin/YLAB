from fastapi import status
from httpx import AsyncClient

from app.main import app


async def test_menu_not_found(client: AsyncClient):
    response = await client.get(
        app.url_path_for('get_menus')
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'menu not found'}


async def test_menu_create(client: AsyncClient, ids: dict):
    payload = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = await client.post(
        app.url_path_for('create_menu'), json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    ids['menu_id'] = response.json()['id']


async def test_get_all_menus(client: AsyncClient, ids: dict):
    response = await client.get(app.url_path_for('get_menus'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': f"{ids['menu_id']}",
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }]


async def test_get_one_menu(client: AsyncClient, ids: dict):
    response = await client.get(
        app.url_path_for('get_menu', id=ids['menu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['menu_id']}",
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


async def test_update_menu(client: AsyncClient, ids: dict):
    payload = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = await client.patch(
        app.url_path_for('update_menu', id=ids['menu_id']),
        json=payload
    )
    # response = await client.patch(f"/api/v1/menus/{ids['menu_id']}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == ids['menu_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']


async def test_changed_one_menu(client: AsyncClient, ids: dict):
    response = await client.get(
        app.url_path_for('get_menu', id=ids['menu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['menu_id']}",
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


async def test_delete_menu(client: AsyncClient, ids: dict):
    response = await client.delete(
        app.url_path_for('del_menu', id=ids['menu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'The menu has been deleted'}
