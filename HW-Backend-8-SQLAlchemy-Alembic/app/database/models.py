from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    profile_photo = Column(String, nullable=True)

    def __repr__(self): 
        return f"<User {self.email}>"
    

class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, index=True)
    cost = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self): 
        return f"<Flower {self.name}>"
    

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    flower_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self): 
        return f"<Purchase {self.name}>"
    


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)  # One cart per user

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    flower_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    