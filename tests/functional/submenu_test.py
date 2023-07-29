from tests.conftest import client


def test_initial_submenu(create_menu_fixture, ids):
    response = client.get("api/v1/menus")
    ids['menu_id'] = str(create_menu_fixture)
    assert response.status_code == 200



def test_submenu_create(ids):
    payload = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = client.post(f"/api/v1/menus/{ids['menu_id']}/submenus", json=payload)
    assert response.status_code == 201
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']
    ids['submenu_id']=response.json()['id']


def test_submenu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}/submenus")
    assert response.status_code == 200
    print('RESPONSE_JSON', response.json())
    assert response.json() == [{
            "id": f"{ids['submenu_id']}",
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "menu_id": f"{ids['menu_id']}",
            "dishes_count": 0
        }]
    

def test_peculiar_submenu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}")
    assert response.status_code == 200
    assert response.json() == {
            "id": f"{ids['submenu_id']}",
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "menu_id": f"{ids['menu_id']}",
            "dishes_count": 0
        }


def test_update_submenu(ids):
    payload = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }
    response = client.patch(f"/api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}", json=payload)
    assert response.status_code == 200
    assert response.json()['id'] == ids['submenu_id']
    assert response.json()['title'] == payload['title']
    assert response.json()['description'] == payload['description']


def test_peculiar_change_submenu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}")
    assert response.status_code == 200
    assert response.json() == {
            "id": f"{ids['submenu_id']}",
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
            "menu_id": f"{ids['menu_id']}",
            "dishes_count": 0
        }
    

def test_delete_menu(ids):
    response = client.delete(f"/api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Successfully deleted data"}


def test_no_found_submenu(ids):
    response = client.get(f"/api/v1/menus/{ids['menu_id']}/submenus/{ids['submenu_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}
