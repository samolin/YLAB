from tests.conftest import client


def test_initial_menu():
    response = client.get('api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


def test_menu_create(ids):
    payload = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post('/api/v1/menus', json=payload)
    assert response.status_code == 201
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    ids['menu_id'] = response.json()['id']


def test_menu(ids):
    response = client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == [{
        'id': f"{ids['menu_id']}",
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }]


def test_peculiar_menu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}")
    assert response.status_code == 200
    assert response.json() == {
        'id': f"{ids['menu_id']}",
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


def test_update_menu(ids):
    payload = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = client.patch(f"/api/v1/menus/{ids['menu_id']}", json=payload)
    assert response.status_code == 200
    assert response.json()['id'] == ids['menu_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']


def test_peculiar_change_menu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}")
    assert response.status_code == 200
    assert response.json() == {
        'id': f"{ids['menu_id']}",
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


def test_delete_menu(ids):
    response = client.delete(f"/api/v1/menus/{ids['menu_id']}")
    assert response.status_code == 200
    assert response.json() == {'message': 'The menu has been deleted'}


def test_cleaned_menu():
    response = client.get('api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


def test_no_found_menu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
