from attrs import define
from sqlalchemy.orm import Session
from app.database.models import Purchase


@define
class PurchaseCreate:
    user_id: int = 0
    flower_id: int = 0
    name: str = ""
    cost: float = 0
    quantity: int = 0


class PurchasesRepository:
    def save_purchase(self, db: Session, user_id: int, cart: list[PurchaseCreate]) -> None:
        for cart_item in cart.items: 

            purchase = Purchase(
                user_id=user_id, 
                flower_id=cart_item.flower_id,
                name = cart_item.name,
                cost=cart_item.cost,
                quantity=cart_item.quantity
            )

            db.add(purchase)
            db.commit()
            db.refresh(purchase)


    def get_purchase(self, db: Session, user_id: int) -> list[Purchase]:
        user_purchases = db.query(Purchase).filter(Purchase.user_id == user_id).all()
        return user_purchases 


    

    
    
    
