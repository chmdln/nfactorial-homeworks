import requests 
from io import BytesIO


BASE_URL = "http://localhost:8000"

def test_signup_endpoint_get():
    """Test the signup page is accessible and returns the signup form."""
    response = requests.get(f"{BASE_URL}/signup")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")
    assert "/signup" in response.text.lower()
    assert "email" in response.text
    assert "full_name" in response.text
    assert "password" in response.text 


def test_signup_endpoint_valid_user():
    """Test successful user signup with valid data."""

    signup_data = {
        "email": f"testuser_1234@example.com",
        "full_name": "Test User",
        "password": "StrongPassword123!"
    }

    response = requests.post(
        f"{BASE_URL}/signup", 
        data=signup_data, 
        allow_redirects=False
    )

    assert response.status_code == 303  
    assert "/login" in response.headers.get("location", "")



def test_signup_endpoint_existing_email():
    """Test signup with an existing email address."""

    signup_data = {
        "email": "testuser_1234@example.com", 
        "full_name": "Existing User",
        "password": "SomePassword123!"
    }

    response = requests.post(
        f"{BASE_URL}/signup", 
        data=signup_data
    )
    
    assert response.status_code == 409  
    assert "already exists" in response.text.lower()



def test_signup_endpoint_with_profile_photo():
    """Test signup with a valid profile photo upload."""

    signup_data = {
        "email": f"photouser_1234@example.com",
        "full_name": "Photo Test User",
        "password": "PhotoPassword123!"
    }
    
    test_image = BytesIO(b"fake image content")
    test_image.name = "test_profile.jpg"
    files = {
        "profile_photo": (test_image.name, test_image, "image/jpeg")
    }

    response = requests.post(
        f"{BASE_URL}/signup", 
        data=signup_data, 
        files=files,
        allow_redirects=False
    )

    assert response.status_code == 303  
    assert "/login" in response.headers.get("location", "")



def test_signup_endpoint_invalid_photo_format():
    """Test signup with an unsupported image format."""

    signup_data = {
        "email": f"invalidphotouser@example.com",
        "full_name": "Invalid Photo User",
        "password": "InvalidPhotoPassword123!"
    }

    test_image = BytesIO(b"fake image content")
    test_image.name = "test_profile.gif"
    
    files = {
        "profile_photo": (test_image.name, test_image, "image/gif")
    }

    response = requests.post(
        f"{BASE_URL}/signup", 
        data=signup_data, 
        files=files
    )
    
    assert response.status_code == 400
    assert "invalid image format" in response.text.lower()



def test_signup_endpoint_missing_required_fields():
    """Test signup with missing required fields."""

    test_cases = [
        {}, 
        {"email": "test@example.com"},  
        {"full_name": "Test User"},  
        {"password": "SomePassword123!"}  
    ]

    for case in test_cases:
        response = requests.post(
            f"{BASE_URL}/signup", 
            data=case
        )
    assert response.status_code == 422


