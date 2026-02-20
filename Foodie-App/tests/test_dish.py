import requests


def test_add_dish(base_url, create_restaurant):
    payload = {
        "name": "Biryani",
        "type": "Non-Veg",
        "price": 250,
        "available_time": "Lunch",
        "image": ""
    }

    response = requests.post(
        f"{base_url}/restaurants/{create_restaurant}/dishes",
        json=payload
    )
    assert response.status_code == 201


def test_update_dish(base_url, create_dish):
    dish_id, _ = create_dish

    response = requests.put(
        f"{base_url}/dishes/{dish_id}",
        json={"price": 200}
    )
    assert response.status_code == 200


def test_enable_disable_dish(base_url, create_dish):
    dish_id, _ = create_dish

    response = requests.put(
        f"{base_url}/dishes/{dish_id}/status",
        json={"enabled": False}
    )
    assert response.status_code == 200


def test_delete_dish(base_url, create_dish):
    dish_id, _ = create_dish

    response = requests.delete(f"{base_url}/dishes/{dish_id}")
    assert response.status_code == 200