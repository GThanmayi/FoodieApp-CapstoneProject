import requests


def test_register_restaurant(base_url, create_restaurant):
    assert create_restaurant is not None


def test_update_restaurant(base_url, create_restaurant):
    response = requests.put(
        f"{base_url}/restaurants/{create_restaurant}",
        json={"location": "Chennai"}
    )
    assert response.status_code == 200


def test_disable_restaurant(base_url, create_restaurant):
    response = requests.put(
        f"{base_url}/restaurants/{create_restaurant}/disable"
    )
    assert response.status_code == 200


def test_view_restaurant_profile(base_url, create_restaurant):
    response = requests.get(
        f"{base_url}/restaurants/{create_restaurant}"
    )
    assert response.status_code == 200