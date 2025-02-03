import requests 
import pytest 
import uuid 
import jwt 
import json 

from datetime import datetime, timedelta, timezone
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

BASE_URL = "http://localhost:8000"


@pytest.fixture
def session():
    return requests.Session()

def create_test_token(user_id: str, secret_key: str = "your_secret_key"):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)


def test_post_purchase_unauthorized():
    """Test saving purchase without access token"""
    response = requests.post(
        f"{BASE_URL}/purchased",
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "Unauthorized" in response.text


def test_post_purchase_invalid_token():
    """Test saving purchase with invalid access token"""
    cookies = {
        "access_token": "invalid_token",
        "cart": "[]"
    }
    response = requests.post(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.text



def test_post_purchase_user_not_found():
    """Test saving purchase with non-existent user"""
    non_existent_user_id = str(uuid.uuid4())
    cookies = {
        "access_token": create_test_token(non_existent_user_id, secret_key=SECRET_KEY),
        "cart": "[]"
    }
    response = requests.post(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "User not found." in response.text



def test_post_purchase_with_invalid_flower():
    """Test saving purchase with non-existent flower in cart"""

    user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7" 
    non_existent_flower_id = str(uuid.uuid4())
    cart_data = [{
        "flower_id": non_existent_flower_id,
        "quantity": "1"
    }]
    
    cookies = {
        "access_token": create_test_token(user_id, secret_key=SECRET_KEY),
        "cart": json.dumps(cart_data)
    }
    
    response = requests.post(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )
    assert response.status_code == 404
    assert f"Flower with id {non_existent_flower_id} not found" in response.text


def test_save_purchase_successful(session):
    """Test successful purchase saving"""

    user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7"  
    data = [{
        "flower_id": "49fa3bb8-9070-422b-adb1-fb8d9dada43b",
        "quantity": 15
    }]
    cookies = {
        "access_token": create_test_token(user_id, secret_key=SECRET_KEY),
        "cart": json.dumps(data)
    }

    response = session.post(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )

    assert response.status_code == 303
    assert "/purchased" in response.headers.get("location", "")


def test_view_purchases_unauthorized():
    """Test viewing purchases without access token"""
    response = requests.get(
        f"{BASE_URL}/purchased",
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "Unauthorized" in response.text


def test_view_purchases_invalid_token():
    """Test viewing purchases with invalid access token"""
    cookies = {
        "access_token": "invalid_token"
    }
    response = requests.get(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.text


def test_view_purchases_user_not_found():
    """Test viewing purchases for non-existent user"""
    non_existent_user_id = str(uuid.uuid4())
    cookies = {
        "access_token": create_test_token(non_existent_user_id, secret_key=SECRET_KEY)
    }
    response = requests.get(
        "http://localhost:8000/purchased",
        cookies=cookies,
        allow_redirects=False
    )
    assert response.status_code == 401
    assert "User not found." in response.text



def test_view_purchases_successful(session):
    """Test successful viewing of purchases"""

    user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7" 
    data = [{
        "flower_id": "49fa3bb8-9070-422b-adb1-fb8d9dada43b",
        "quantity": 15
    }]
    cookies = {
        "access_token": create_test_token(user_id, secret_key=SECRET_KEY),
        "cart": json.dumps(data)
    }

    session.post(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )    
    
    response = session.get(
        f"{BASE_URL}/purchased",
        cookies=cookies,
        allow_redirects=False
    )

    assert response.status_code == 200
    assert "text/html" in response.headers.get('content-type', "")
    assert "Roses" in response.text  
    assert "25.99" in response.text 
    assert "15" in response.text  