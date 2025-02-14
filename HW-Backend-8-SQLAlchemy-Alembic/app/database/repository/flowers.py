from attrs import define
from sqlalchemy.orm import Session
from app.database.models import Flower

@define
class FlowerCreate:
    name: str
    count: int
    cost: int

@define 
class FlowerUpdate(FlowerCreate):
    pass 
    



class FlowersRepository:

    def get_all_flowers(self, db: Session) -> list[Flower]:
        flowers = db.query(Flower).all()
        return flowers

    def add_flower(self, db: Session, flower: FlowerCreate) -> Flower: 
        existing_flower = db.query(Flower).filter(Flower.name == flower.name).first()
        if existing_flower: 
            return {"error": "Flower already exists"}
        
        flower_db = Flower(
            name=flower.name,  
            cost=flower.cost,
            count=flower.count,
        )
        
        db.add(flower_db)
        db.commit()
        db.refresh(flower_db)
        return flower_db 
    

    def update_flower(self, db: Session, flower_id: str, flower: FlowerUpdate) -> Flower:
        flower_db = db.query(Flower).filter(Flower.id == flower_id).first()
        if not flower_db: 
            return {"error": "Flower not found"}
        
        flower_db.name = flower.name
        flower_db.cost = flower.cost
        flower_db.count = flower.count

        db.commit()
        db.refresh(flower_db)
        return flower_db    

    def delete_flower(self, db: Session, flower_id: str): 
        flower_db = db.query(Flower).filter(Flower.id == flower_id).first()
        if not flower_db: 
            return {"error": "Flower not found"}
        db.delete(flower_db)
        db.commit()
        return {"message": "Flower deleted"}


    def get_flower_by_id(self, db: Session, flower_id: str) -> Flower:
        flower_db = db.query(Flower).filter(Flower.id == flower_id).first()
        if flower_db: 
            return flower_db 
        return None

        
    
