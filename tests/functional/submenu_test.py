from fastapi import status
from httpx import AsyncClient

from app.main import app


async def test_submenu_not_found(client: AsyncClient, ids: dict, create_menu_fixture):
    ids['menu_id'] = create_menu_fixture
    response = await client.get(
        app.url_path_for('get_submenus', id=ids['menu_id'])
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'submenu not found'}


async def test_submenu_create(client: AsyncClient, ids: dict):
    payload = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': f"{ids['menu_id']}"
    }
    response = await client.post(
        app.url_path_for('create_submenu', id=ids['menu_id']),
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    ids['submenu_id'] = response.json()['id']


async def test_get_all_submenus(client: AsyncClient, ids: dict):
    response = await client.get(
        app.url_path_for('get_submenus', id=ids['menu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': f"{ids['submenu_id']}",
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': f"{ids['menu_id']}",
        'dishes_count': 0
    }]


async def test_get_one_submenu(client: AsyncClient, ids):
    response = await client.get(
        app.url_path_for('get_submenu', id=ids['menu_id'], sub_id=ids['submenu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['submenu_id']}",
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': f"{ids['menu_id']}",
        'dishes_count': 0
    }


async def test_update_submenu(client: AsyncClient, ids):
    payload = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
        'menu_id': f"{ids['menu_id']}",
    }
    response = await client.patch(
        app.url_path_for('update_submenu', id=ids['menu_id'], sub_id=ids['submenu_id']),
        json=payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == ids['submenu_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    assert response.json()['menu_id'] == payload['menu_id']


async def test_changed_one_submenu(client: AsyncClient, ids):
    response = await client.get(
        app.url_path_for('get_submenu', id=ids['menu_id'], sub_id=ids['submenu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['submenu_id']}",
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
        'menu_id': f"{ids['menu_id']}",
        'dishes_count': 0
    }


async def test_delete_submenu(client: AsyncClient, ids):
    response = await client.delete(
        app.url_path_for('del_submenu', id=ids['menu_id'], sub_id=ids['submenu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'msg': 'Successfully deleted data'}
