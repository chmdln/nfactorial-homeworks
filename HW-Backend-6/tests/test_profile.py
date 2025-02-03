import pytest 
import requests 
from datetime import datetime, timedelta, timezone
import jwt
import uuid 
from app.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


BASE_URL = "http://localhost:8000"

def create_test_token(user_id: str, expired: bool = False) -> str:
    """Helper function to create test JWT tokens"""
    if expired:
        exp = datetime.now(timezone.utc) - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(user_id),
        "exp": exp
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def test_profile_success():
    """Test successful profile access with valid token"""

    session = requests.Session()
    test_user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7"
    valid_token = create_test_token(test_user_id)
    session.cookies.set("access_token", valid_token)
    response = session.get(f"{BASE_URL}/profile")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "User's profile" in response.text
    assert "User id: cd3374d0-a263-4d4d-a8c8-580116fad2e7" in response.text
    assert "Full name: John Doe" in response.text
    assert "Email: 7GxkZ@example.com" in response.text
    

def test_profile_no_token():
    """Test profile access without token"""
    
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401
    assert "unauthorized" in response.text.lower()


def test_profile_expired_token():
    """Test profile access with expired token"""
    
    test_user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7"
    expired_token = create_test_token(test_user_id, expired=True)
    session = requests.Session()
    session.cookies.set("access_token", expired_token)
    response = session.get(f"{BASE_URL}/profile")

    assert response.status_code == 401
    assert "Bearer" in response.headers.get("WWW-Authenticate", "")
    assert "Could not validate credentials" in response.text


def test_profile_invalid_token():
    """Test profile access with malformed token"""
    
    session = requests.Session()
    session.cookies.set("access_token", "invalid-token-string")
    response = session.get(f"{BASE_URL}/profile")
    
    assert response.status_code == 401
    assert "Bearer" in response.headers.get("WWW-Authenticate", "")
    assert "Could not validate credentials" in response.text


def test_profile_nonexistent_user():
    """Test profile access with valid token but non-existent user"""

    nonexistent_user_id = str(uuid.uuid4())
    valid_token = create_test_token(nonexistent_user_id)
    session = requests.Session()
    session.cookies.set("access_token", valid_token)
    response = session.get(f"{BASE_URL}/profile")
    
    assert response.status_code == 401
    assert "User not found" in response.text


@pytest.fixture
def authenticated_session():
    session = requests.Session()
    test_user_id = "cd3374d0-a263-4d4d-a8c8-580116fad2e7"
    valid_token = create_test_token(test_user_id)
    session.cookies.set("access_token", valid_token)
    return session


def test_profile_multiple_requests(authenticated_session):
    """Test multiple profile requests with same session"""
    for _ in range(3):
        response = authenticated_session.get(f"{BASE_URL}/profile")

        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "User's profile" in response.text
        assert "cd3374d0-a263-4d4d-a8c8-580116fad2e7" in response.text
        assert "John Doe" in response.text
        assert "7GxkZ@example.com" in response.text
