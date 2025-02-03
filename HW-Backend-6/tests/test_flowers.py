import requests

BASE_URL = "http://localhost:8000"

def test_get_flowers_existing():
    """Test getting flowers with pre-existing data"""
    response = requests.get(f"{BASE_URL}/flowers")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Add flower" in response.text
    assert "/flowers" in response.text 
    assert "name" in response.text
    assert "cost" in response.text
    assert "count" in response.text
    assert "List of flowers" in response.text
    assert "Roses" in response.text
    assert "$25.99" in response.text
    assert "flower_id" in response.text
    assert "8efdaded-3755-4e30-aa14-a696b124c869"
    assert "100" in response.text
    


def test_get_flowers_with_content():
    """Test getting flowers after adding a flower"""

    test_data = {
        "name": "Orchids", 
        "count": 10, 
        "cost": 2.50
    }

    requests.post(f"{BASE_URL}/flowers", data=test_data)
    response = requests.get(f"{BASE_URL}/flowers")

    assert response.status_code == 200
    assert "Orchids" in response.text
    assert "$2.5" in response.text
    assert "10" in response.text



def test_post_flower_valid():
    """Test adding a valid flower"""
    data = {
        "name": "Daisies", 
        "count": 125, 
        "cost": 1.99
    }
    response = requests.post(
        f"{BASE_URL}/flowers",
        data=data,
        allow_redirects=False
    )
    
    assert response.status_code == 303
    assert "/flowers" in response.headers.get("location", "")



def test_post_flower_missing_fields():
    """Test adding a flower with missing required fields"""

    data = {"name": "Lilies"}
    response = requests.post(f"{BASE_URL}/flowers", data=data)

    assert response.status_code == 422
    assert '"type":"missing"' in response.text
    assert '"msg":"Field required"' in response.text 



def test_post_duplicate_flower():
    """Test adding a flower that already exists"""
    data = {
        "name": "Tulips", 
        "count": 3, 
        "cost": 3.99
    }
    
    response = requests.post(
        f"{BASE_URL}/flowers",
        data=data,
        allow_redirects=False
    )

    assert response.status_code == 409
    assert "Flower with name Tulips already exists." in response.text
    