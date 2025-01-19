import requests


def test_contains_form():
    response = requests.get("http://localhost:8000/cars/search")
    assert "form" in response.text


def test_cars_search():
    response = requests.get("http://localhost:8000/cars/search")
    assert "Mitsubishi" in response.text
    assert "Lexus LX" in response.text


def test_cars_search_starts_with():
    response = requests.get("http://localhost:8000/cars/search?car_name=kia")
    assert "Ford Taurus" not in response.text
    assert "Kia Sedona" in response.text
    assert "Kia Sorento" in response.text


def test_cars_search_in_middle():
    response = requests.get("http://localhost:8000/cars/search?car_name=regular")
    assert "Ford Focus ST" not in response.text
    assert "Chevrolet Silverado 3500 HD Regular Cab" in response.text
    assert "Ford Ranger Regular Cab" in response.text
    assert "Ford F350 Super Duty Regular Cab" in response.text
    assert "GMC 3500 Regular Cab" in response.text
    assert "Toyota Tundra Regular Cab" in response.text
    assert "Isuzu Hombre Regular Cab" in response.text


def test_cars_search_not_found():
    response = requests.get("http://localhost:8000/cars/search?car_name=aaaaa'")
    assert "aaaaa" in response.text