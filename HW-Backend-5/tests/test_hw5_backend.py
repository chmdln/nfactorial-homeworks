import requests


def test_edit_book_form_has_form():
    response = requests.get("http://localhost:8000/books/3/edit")
    assert "title" in response.text
    assert "author" in response.text
    assert "year" in response.text
    assert "total_pages" in response.text
    assert "genre" in response.text
    assert "Update" in response.text


def test_edit_book_form_has_values():
    response = requests.get("http://localhost:8000/books/4/edit")    
    assert "The Lord of the Rings" in response.text  
    assert "J.R.R. Tolkien" in response.text
    assert "1954" in response.text
    assert "1178" in response.text
    assert "Fantasy" in response.text         


def test_edit_book_form_not_found(): 
    response = requests.get("http://localhost:8000/books/100/edit")
    assert response.status_code == 404


def test_edit_book_empty_fields():
    data = {"title": "",
            "author": "Dostoyevsky",
            "year": "",
            "total_pages": 1456,
            "genre": "Novel"}
    
    response = requests.post("http://localhost:8000/books/1/edit", data=data)
    assert response.status_code == 422


def test_edit_book_success_redirect():
    data = {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "total_pages": 281,
        "genre": "Fiction, Southern Gothic"
    }

    response = requests.post(
        "http://localhost:8000/books/1/edit", data=data, allow_redirects=False
    )
    assert response.status_code == 303


def test_edit_book_success_has_values():
    response = requests.get("http://localhost:8000/books/1")
    assert "To Kill a Mockingbird" in response.text  
    assert "Harper Lee" in response.text
    assert "1960" in response.text
    assert "281" in response.text
    assert "Fiction, Southern Gothic" in response.text  


def test_get_book_by_id_not_found():
    response = requests.get("http://localhost:8000/books/199")
    assert response.status_code == 404


def test_delete_book_has_form():
    response = requests.get("http://localhost:8000/books/4")
    assert "The Lord of the Rings" in response.text
    assert "J.R.R. Tolkien" in response.text
    assert "1954" in response.text
    assert "1178" in response.text
    assert "Fantasy" in response.text
    assert "/delete" in response.text 


def test_delete_book_success_redirect():
    response = requests.post(
        "http://localhost:8000/books/3/delete", allow_redirects=False
    )
    assert response.status_code == 303


def test_delete_book_success_has_values():
    response = requests.get("http://localhost:8000/books")
    assert "The Great Gatsby" not in response.text
    assert "F. Scott Fitzgerald" not in response.text
    assert "1925" not in response.text
    assert "180" not in response.text
    assert "Classic" not in response.text


