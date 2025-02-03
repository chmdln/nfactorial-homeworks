import requests 
import jwt 


BASE_URL = "http://localhost:8000"


def test_get_login():
    """Test login page rendering"""
    response = requests.get(f"{BASE_URL}/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "/login" in response.text.lower()
    assert "email" in response.text
    assert "password" in response.text



def test_login_success():
    """Test successful login with valid credentials"""
    data = {
        "email": "7GxkZ@example.com",
        "password": "password123"
    }

    response = requests.post(
        f"{BASE_URL}/login",
        data=data,
        allow_redirects=False
    )

    assert response.status_code == 303
    assert "/profile" in response.headers.get("location", "")
    assert "access_token" in response.cookies
    
    token = response.cookies.get("access_token", "")
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert "sub" in decoded
    assert "exp" in decoded


def test_login_nonexistent_user():
    """Test login with non-existent email"""
    data = {
        "email": "nonexistent@example.com",
        "password": "anypassword"
    }
    
    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 401
    assert "does not exist" in response.text.lower()


def test_login_wrong_password():
    """Test login with incorrect password"""
    data = {
        "email": "7GxkZ@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 401
    assert "incorrect" in response.text.lower()



def test_login_missing_fields():
    """Test login with missing required fields"""
    test_cases = [
        {},
        {"email": ""},
        {"password": ""},
        {"email": "test@example.com"},
        {"password": "testpass"}
    ]
    
    for case in test_cases:
        response = requests.post(f"{BASE_URL}/login", data=case)
        assert response.status_code == 422
        assert '"msg":"Field required"' in response.text


