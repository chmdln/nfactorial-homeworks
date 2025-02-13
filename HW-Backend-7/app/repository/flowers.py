import uuid
from attrs import define

@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0
    quantity: int = 0


class FlowersRepository:
    def __init__(self):
        self.flowers: list[Flower] = [
            Flower(
                name="Roses",  
                cost=25.99,
                count=50,
                id=uuid.UUID('49fa3bb8-9070-422b-adb1-fb8d9dada43b')
            ),
            Flower(
                name="Tulips",  
                cost=15.05,  
                count=100,
                id=uuid.UUID('8efdaded-3755-4e30-aa14-a696b124c869')
            )
        ]

    def add_flower(self, name: str, cost: int, count: int) -> Flower: 
        for flower in self.flowers:
            if flower.name.lower() == name.lower():
                return {"error": "Flower already exists"}
        
        flower = Flower(
            name=name,  
            cost=cost,
            count=count,
            id=self.generate_id()
        )
        
        self.flowers.append(flower)
        return flower

    def get_flower_by_id(self, flower_id: str) -> Flower:
        for flower in self.flowers:
            if flower.id == flower_id:
                return flower 
        return None
    
    def generate_id(self) -> uuid.UUID:
        id = uuid.uuid4()
        return id
        
    
