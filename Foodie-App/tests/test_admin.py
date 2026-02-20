import requests


def test_admin_approve_restaurant(base_url, create_restaurant):
    response = requests.put(
        f"{base_url}/admin/restaurants/{create_restaurant}/approve"
    )
    assert response.status_code == 200


def test_admin_disable_restaurant(base_url, create_restaurant):
    response = requests.put(
        f"{base_url}/admin/restaurants/{create_restaurant}/disable"
    )
    assert response.status_code == 200


def test_view_feedback(base_url):
    response = requests.get(f"{base_url}/admin/feedback")
    assert response.status_code == 200


def test_view_order_status(base_url):
    response = requests.get(f"{base_url}/admin/orders")
    assert response.status_code == 200