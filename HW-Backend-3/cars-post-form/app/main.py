from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from .repository import CarsRepository

app = FastAPI()

templates = Jinja2Templates(directory="templates")
repository = CarsRepository()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cars")
def get_cars(request: Request):
    cars = repository.get_all()
    return templates.TemplateResponse(
        "cars/index.html",
        {"request": request, "cars": cars},
    )

@app.get("/cars/new")
def add_car(request: Request):
    return templates.TemplateResponse("cars/new.html", {"request": request})


@app.post("/cars/new")
def save_car(request: Request, name: str = Form(...), year: str = Form(...)):
    if not name or not year:
        raise HTTPException(status_code=422, detail="Name and year are required.")
    
    id = repository.get_next_id()
    repository.save({"id": id,
                     "name": name.lower().title(), 
                     "year": year
    })
    return RedirectResponse(url="/cars", status_code=303)

