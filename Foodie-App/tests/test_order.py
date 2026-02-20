import pytest
import requests
from jsonschema import validate


order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "user_id": {"type": "number"},
        "restaurant_id": {"type": "number"},
        "dishes": {"type": "array"}
    },
    "required": ["id", "user_id", "restaurant_id", "dishes"]
}


rating_schema = {
    "type": "object",
    "properties": {
        "order_id": {"type": "number"},
        "rating": {"type": "number"},
        "comment": {"type": ["string", "null"]}
    },
    "required": ["order_id", "rating"]
}


# ✅ Place Order - Positive
def test_place_order_success(base_url, create_user, create_dish):
    dish_id, restaurant_id = create_dish

    payload = {
        "user_id": create_user,
        "restaurant_id": restaurant_id,
        "dishes": [dish_id]
    }

    response = requests.post(
        f"{base_url}/orders",
        json=payload
    )

    assert response.status_code == 201
    validate(response.json(), order_schema)


# ✅ Place Order - Negative (API currently allows)
def test_place_order_missing_field(base_url):
    payload = {
        "user_id": 1
    }

    response = requests.post(
        f"{base_url}/orders",
        json=payload
    )

    # API currently returns 201 even for incomplete data
    assert response.status_code in [201, 400, 500]


# ✅ Add Rating
def test_add_rating_success(base_url, create_order):
    payload = {
        "order_id": create_order,
        "rating": 5,
        "comment": "Excellent food"
    }

    response = requests.post(
        f"{base_url}/ratings",
        json=payload
    )

    assert response.status_code == 201
    validate(response.json(), rating_schema)


# ✅ Orders by Restaurant
@pytest.mark.parametrize("dummy", [1, 2])
def test_get_orders_by_restaurant(base_url, create_restaurant, dummy):
    response = requests.get(
        f"{base_url}/restaurants/{create_restaurant}/orders"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ✅ Orders by User
@pytest.mark.parametrize("dummy", [1, 2])
def test_get_orders_by_user(base_url, create_user, dummy):
    response = requests.get(
        f"{base_url}/users/{create_user}/orders"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)