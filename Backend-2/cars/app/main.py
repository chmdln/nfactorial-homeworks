from fastapi import FastAPI, Response, Query

from .cars import create_cars

cars = create_cars(100)  # Здесь хранятся список машин
app = FastAPI()



@app.get("/")
def index():
    return Response("<a href='/cars'>Cars</a>")


@app.get("/cars")
def get_cars(page: int = Query(1, gt=0), limit: int = Query(10, gt=0)):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]


@app.get("/cars/{id}")
def get_car_by_id(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    return Response(content="Not found", status_code=404)

