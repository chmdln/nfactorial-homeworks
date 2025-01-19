import requests


def test_has_form():
    response = requests.get("http://localhost:8000/cars/new")
    assert "name" in response.text
    assert "year" in response.text


def test_validate_empty_form():
    data = {"name": ""}
    response = requests.post("http://localhost:8000/cars/new", data=data)
    assert response.status_code == 422


def test_validate_empty_year():
    data = {"name": "BMW"}
    response = requests.post("http://localhost:8000/cars/new", data=data)
    assert response.status_code == 422


def test_validate_empty_name():
    data = {"name": "", "year": 2000}
    response = requests.post("http://localhost:8000/cars/new", data=data)
    assert response.status_code == 422


def test_post():
    data = {"name": "Kia Rio", "year": 2023}
    response = requests.post(
        "http://localhost:8000/cars/new", data=data, allow_redirects=False
    )
    assert response.status_code == 303