import requests


def test_user_registration(create_user):
    assert create_user is not None


def test_search_restaurants(base_url):
    response = requests.get(
        f"{base_url}/restaurants/search?location=Hyderabad"
    )
    assert response.status_code == 200


def test_place_order(base_url, create_user, create_dish):
    dish_id, restaurant_id = create_dish

    response = requests.post(
        f"{base_url}/orders",
        json={
            "user_id": create_user,
            "restaurant_id": restaurant_id,
            "dishes": [dish_id]
        }
    )

    assert response.status_code == 201


def test_give_rating(base_url, create_order):
    response = requests.post(
        f"{base_url}/ratings",
        json={
            "order_id": create_order,
            "rating": 5,
            "comment": "Excellent"
        }
    )

    assert response.status_code in [201, 400]


def test_view_orders_by_user(base_url, create_user):
    response = requests.get(
        f"{base_url}/users/{create_user}/orders"
    )
    assert response.status_code == 200