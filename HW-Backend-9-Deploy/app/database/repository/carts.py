from attrs import define
from sqlalchemy.orm import Session
from app.database.models import Cart, CartItem

@define
class AddToCart:
    user_id: int
    flower_id: int
    quantity: int


class CartsRepository: 
    def add_to_cart(self, db: Session, cart: AddToCart) -> Cart:
        cart_db = db.query(Cart).filter(Cart.user_id == cart.user_id).first()
        if cart_db is None:
            cart_db = Cart(user_id=cart.user_id)
            db.add(cart_db)
            db.commit()
            db.refresh(cart_db)

        cart_item = CartItem(
            cart_id=cart_db.id,
            flower_id=cart.flower_id,
            quantity=cart.quantity
        )

        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        cart_db.items.append(cart_item)
        return cart_db
    

    def get_cart(self, db: Session, user_id: int) -> Cart:
        cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
        if cart_db: 
            return cart_db
        return None 

