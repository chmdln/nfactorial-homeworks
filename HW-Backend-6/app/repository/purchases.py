from attrs import define


@define
class Purchase:
    user_id: int = 0
    flower_id: int = 0
    name: str = ""
    cost: float = 0
    quantity: int = 0


class PurchasesRepository:
    def __init__(self):
        self.purchases: list[Purchase]= []

    def save_purchase(self, user_id: int, cart: list[dict]) -> None:
        for cart_item in cart: 

            purchase = Purchase(
                user_id=user_id, 
                flower_id=cart_item["flower_id"],
                name = cart_item["name"],
                cost=cart_item["cost"],
                quantity=cart_item["quantity"]
            )
            self.purchases.append(purchase)


    def get_purchase(self, user_id: int) -> list[Purchase]:
        user_purchases = []
        for purchase in self.purchases:
            if purchase.user_id == user_id:
                user_purchases.append(purchase)
        return user_purchases 


    

    
    
    
