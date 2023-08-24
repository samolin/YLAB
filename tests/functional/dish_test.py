from fastapi import status
from httpx import AsyncClient

from app.main import app


async def test_dish_not_found(client: AsyncClient, ids: dict, create_submenu_fixture):
    ids['menu_id'], ids['submenu_id'] = map(str, create_submenu_fixture)
    response = await client.get(
        app.url_path_for('get_dishes', id=ids['menu_id'], sub_id=ids['submenu_id'])
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'dish not found'}


async def test_dish_create(client: AsyncClient, ids: dict):
    payload = {
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'price': 20,
        'submenu_id': f"{ids['submenu_id']}"
    }
    response = await client.post(
        app.url_path_for('create_dish', id=ids['menu_id'], sub_id=ids['submenu_id']),
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    assert response.json()['price'] == '{:.2f}'.format(payload['price'])
    assert response.json()['submenu_id'] == ids['submenu_id']
    ids['dish_id'] = response.json()['id']


async def test_get_all_dishes(client: AsyncClient, ids: dict):
    response = await client.get(
        app.url_path_for('get_dishes', id=ids['menu_id'], sub_id=ids['submenu_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': f"{ids['dish_id']}",
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'price': '20.00',
        'submenu_id': f"{ids['submenu_id']}",
    }]


async def test_get_one_dish(client: AsyncClient, ids: dict):
    response = await client.get(
        app.url_path_for('get_dish', id=ids['menu_id'], sub_id=ids['submenu_id'], dish_id=ids['dish_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['dish_id']}",
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'price': '20.00',
        'submenu_id': f"{ids['submenu_id']}"
    }


async def test_update_dish(client: AsyncClient, ids):
    payload = {
        'title': 'My updated new dish 1',
        'description': 'Description for updated dish 1',
        'price': 823,
        'submenu_id': str(ids['submenu_id'])
    }
    response = await client.patch(
        app.url_path_for('update_dish', id=ids['menu_id'], sub_id=ids['submenu_id'], dish_id=ids['dish_id']),
        json=payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == ids['dish_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    assert response.json()['price'] == '{:.2f}'.format(payload['price'])
    assert response.json()['submenu_id'] == payload['submenu_id']


async def test_peculiar_change_dish(client: AsyncClient, ids):
    response = await client.get(
        app.url_path_for('get_dish', id=ids['menu_id'], sub_id=ids['submenu_id'], dish_id=ids['dish_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': f"{ids['dish_id']}",
        'title': 'My updated new dish 1',
        'description': 'Description for updated dish 1',
        'price': '823.00',
        'submenu_id': f"{ids['submenu_id']}"
    }


async def test_delete_dish(client: AsyncClient, ids):
    response = await client.delete(
        app.url_path_for('get_dish', id=ids['menu_id'], sub_id=ids['submenu_id'], dish_id=ids['dish_id'])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'msg': 'Successfully deleted data'}
