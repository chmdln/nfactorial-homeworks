import pytest 
import requests
import uuid 


BASE_URL = "http://localhost:8000"

@pytest.fixture
def session():
    return requests.Session()
    


def test_add_to_cart_valid(session):
    """Test adding a valid item to cart"""
    data = {
        "flower_id": "49fa3bb8-9070-422b-adb1-fb8d9dada43b",
        "quantity": 2
    }
    response = session.post(
        f"{BASE_URL}/cart/items",
        data=data,
        allow_redirects=False
    )

    assert response.status_code == 303
    assert "/flowers" in response.headers.get("location")
    assert "cart" in response.cookies
    assert "49fa3bb8-9070-422b-adb1-fb8d9dada43b" in response.cookies["cart"]
    assert "2" in response.cookies["cart"]



def test_add_to_cart_excessive_quantity(session):
    """Test adding item with quantity exceeding available stock"""
    data = {
        "flower_id": "8efdaded-3755-4e30-aa14-a696b124c869",
        "quantity": "101"  
    }
    response = session.post(
        f"{BASE_URL}/cart/items",
        data=data,
        allow_redirects=False
    )

    assert response.status_code == 400
    assert "Invalid quantity." in response.text



def test_add_to_cart_invalid_flower_id(session):
    """Test adding non-existent flower to cart"""
    data = {
        "flower_id": str(uuid.uuid4()),  
        "quantity": "1"
    }
    response = session.post(
        f"{BASE_URL}/cart/items",
        data=data,
        allow_redirects=False
    )

    assert response.status_code == 404
    assert f"Flower with id {data["flower_id"]} not found." in response.text


def test_view_empty_cart(session):
    """Test viewing an empty cart"""
    response = session.get(f"{BASE_URL}/cart/items")
    
    assert response.status_code == 200
    assert "Cart items:" in response.text 
    assert "Cart total: $0" in response.text
    assert "Purchase" in response.text



def test_view_cart_with_items(session):
    """Test viewing cart with items"""
    data = {
        "flower_id": "8efdaded-3755-4e30-aa14-a696b124c869",
        "quantity": "27"
    }
    session.post(
        f"{BASE_URL}/cart/items",
        data=data,
        allow_redirects=False
    )
    response = session.get(f"{BASE_URL}/cart/items")

    assert response.status_code == 200
    assert "Cart items:" in response.text
    assert "8efdaded-3755-4e30-aa14-a696b124c869" in response.text
    assert "Tulips" in response.text
    assert "15.05" in response.text  
    assert "27" in response.text
    assert "Cart total: $406.35" in response.text




