from tests.conftest import client


def test_initial_dish(create_submenu_fixture, ids):
    response = client.get('api/v1/menus')
    ids['menu_id'], ids['submenu_id'] = map(str, create_submenu_fixture)
    assert response.status_code == 200


def test_dish_create(ids):
    payload = {
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'price': 20
    }
    response = client.post(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes", json=payload)
    assert response.status_code == 201
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    assert response.json()['price'] == '{:.2f}'.format(payload['price'])
    ids['dish_id'] = response.json()['id']


def test_dish(ids):
    response = client.get(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() == [{
        'id': f"{ids['dish_id']}",
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'submenu_id': f"{ids['submenu_id']}",
        'price': 20.0,
    }]


def test_peculiar_dish(ids):
    response = client.get(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes/{ids['dish_id']}")
    assert response.status_code == 200
    assert response.json() == {
        'id': f"{ids['dish_id']}",
        'title': 'My dish 1',
        'description': 'Description for dish 1',
        'price': '20.00'
    }


def test_update_dish(ids):
    payload = {
        'title': 'My new dish 1',
        'description': 'Description for fish dish 1',
        'price': 823
    }
    response = client.patch(
        f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes/{ids['dish_id']}", json=payload)
    assert response.status_code == 200
    assert response.json()['id'] == ids['dish_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    assert response.json()['price'] == '{:.2f}'.format(payload['price'])


def test_peculiar_change_dish(ids):
    response = client.get(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes/{ids['dish_id']}")
    assert response.status_code == 200
    assert response.json() == {
        'id': f"{ids['dish_id']}",
        'title': 'My new dish 1',
        'description': 'Description for fish dish 1',
        'price': '823.00'
    }


def test_delete_dish(ids):
    response = client.delete(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes/{ids['dish_id']}")
    assert response.status_code == 200
    assert response.json() == {'msg': 'Successfully deleted data'}


def test_no_found_dish(ids):
    response = client.get(f"api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}/dishes/{ids['dish_id']}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}
