from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from .repository import BooksRepository

app = FastAPI()

templates = Jinja2Templates(directory="templates")
repository = BooksRepository()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/books")
def get_books(request: Request, page:int|None = 1):
    
    limit = 10
    start = (page - 1) * limit
    books = repository.get_all()[start:start+limit]
    
    return templates.TemplateResponse(
        "books/index.html",
        {
            "request": request, 
            "books": books, 
            "current_page": page,
            "total_pages": (len(repository.get_all()) + limit - 1) // limit
        }
    )


@app.get("/books/new")
def add_book_form(request: Request):
    return templates.TemplateResponse(
        "books/new.html", 
        {
            "request": request
        }
    )


@app.post("/books")
def add_book(request: Request, 
             title: str = Form(...), 
             author: str = Form(...), 
             year: int = Form(...), 
             total_pages: int = Form(...), 
             genre: str = Form(...)): 
    
    book = {
        "title": title, 
        "author": author, 
        "year": year, 
        "total_pages": total_pages, 
        "genre": genre
    }
    repository.save(book)

    return RedirectResponse(url="/books", status_code=303)




#####################  HW-5-Backend  #####################

@app.get("/books/{id}")
def get_book_by_id(request: Request, id: int):
    book = repository.get_one(id)

    if book is None:
        return Response(content="Not Found", status_code=404)
    
    return templates.TemplateResponse(
        "books/show.html", 
        {
            "request": request, 
            "book": book
        }
    )


@app.get("/books/{id}/edit")
def edit_book_form(request: Request, id: int):
    book = repository.get_one(id)

    if book is None:
        return Response(content="Not Found", status_code=404)
    
    return templates.TemplateResponse(
        "books/edit.html", 
        {
            "request": request, 
            "book": book
        }
    )


@app.post("/books/{id}/edit")
def edit_book(request: Request, 
              id: int, 
              title: str = Form(...), 
              author: str = Form(...), 
              year: int = Form(...), 
              total_pages: int = Form(...), 
              genre: str = Form(...)): 
    
    book = {
        "id": id, 
        "title": title, 
        "author": author, 
        "year": year, 
        "total_pages": total_pages, 
        "genre": genre
    }
    response = repository.update(id, book)

    if response is None:
        return Response(content="Not Found", status_code=404)
    return RedirectResponse(url=f"/books/{id}", status_code=303)



@app.post("/books/{id}/delete")
def delete_book(request: Request, id: int):
    response = repository.delete(id)

    if response is None:
        return Response(content="Not Found", status_code=404)
    return RedirectResponse(url="/books", status_code=303) 


#####################  HW-5-Backend  #####################