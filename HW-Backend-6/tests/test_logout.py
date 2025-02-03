import requests

BASE_URL = "http://localhost:8000"



def test_logout_redirect():
    """Test that logout endpoint redirects to login page"""
    
    response = requests.post(f"{BASE_URL}/logout", allow_redirects=False)
    assert response.status_code == 303
    assert response.headers.get("location", "") == "/login"


def test_logout_subsequent_requests():
    """Test that response contains Set-Cookie headers that remove cookies"""
    
    session = requests.Session()
    session.cookies.set("access_token", "test-token")
    session.cookies.set("cart", "test-cart-items")
    response = session.post(f"{BASE_URL}/logout", allow_redirects=False)
    set_cookie_headers = response.headers.get("Set-Cookie", "")
    
    assert 'access_token="";' in set_cookie_headers
    assert 'cart="";' in set_cookie_headers
    assert "Max-Age=0" in set_cookie_headers  



    

