from fastapi import FastAPI, Request
from cars import create_cars
from fastapi.templating import Jinja2Templates

app = FastAPI(tags=["cars"])
templates = Jinja2Templates(directory="templates")
cars = create_cars(100)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/cars/search")
def search_cars(request: Request, car_name: str = None): 
    
    filtered_cars = []
    if car_name:
        car_name_lower = car_name.lower()
        filtered_cars = [car for car in cars if car_name_lower in car["name"].lower()]
    else:
        filtered_cars = cars
    return templates.TemplateResponse("cars/search.html", {"request": request, 
                                                           "cars": filtered_cars, 
                                                           "car_name": car_name}) 

