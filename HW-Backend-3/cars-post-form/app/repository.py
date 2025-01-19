class CarsRepository:
    def __init__(self):
        self.cars = [
            {"id": 1, "name": "Land Rover Range Rover", "year": "2018"},
            {"id": 2, "name": "Ford Thunderbird", "year": "2011"},
            {"id": 3, "name": "GMC 3500 Club Coupe", "year": "2010"},
            {"id": 4, "name": "Toyota 4Runner", "year": "2002"},
            {"id": 5, "name": "Chevrolet Express 2500 Passenger", "year": "2009"},
        ]

    def get_all(self):
        return self.cars

    def get_one(self, car_id):
        for car in self.cars:
            if car["id"] == car_id:
                return car
        return None

    def save(self, car):
        if "id" not in car or not car["id"]:
            car["id"] = self.get_next_id()
        self.cars.append(car)
        return car

    def get_next_id(self):
        return len(self.cars) + 1