import pytest
import requests
import uuid

BASE_URL = "http://127.0.0.1:5000/api/v1"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def create_user(base_url):
    payload = {
        "name": "TestUser",
        "email": f"user_{uuid.uuid4()}@gmail.com",
        "password": "12345"
    }
    response = requests.post(f"{base_url}/users/register", json=payload)
    assert response.status_code in [200, 201]
    return response.json()["id"]


@pytest.fixture
def create_restaurant(base_url):
    payload = {
        "name": f"Res_{uuid.uuid4()}",
        "category": "Indian",
        "location": "Hyderabad",
        "images": [],
        "contact": "9999999999"
    }
    response = requests.post(f"{base_url}/restaurants", json=payload)
    assert response.status_code in [200, 201]
    return response.json()["id"]


@pytest.fixture
def create_dish(base_url, create_restaurant):
    payload = {
        "name": "TestDish",
        "type": "Veg",
        "price": 150,
        "available_time": "Lunch",
        "image": ""
    }

    response = requests.post(
        f"{base_url}/restaurants/{create_restaurant}/dishes",
        json=payload
    )

    assert response.status_code in [200, 201]
    return response.json()["id"], create_restaurant


@pytest.fixture
def create_order(base_url, create_user, create_dish):
    dish_id, restaurant_id = create_dish

    payload = {
        "user_id": create_user,
        "restaurant_id": restaurant_id,
        "dishes": [dish_id]
    }

    response = requests.post(f"{base_url}/orders", json=payload)
    assert response.status_code in [200, 201]

    return response.json()["id"]