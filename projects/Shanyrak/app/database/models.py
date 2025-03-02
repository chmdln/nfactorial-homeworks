from sqlalchemy import (
    Column, Integer, Float, ForeignKey, 
    Text, String, DateTime, func
)
from sqlalchemy.orm import relationship
from app.database.database import Base 

class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationship to listings
    listings = relationship("Listing", back_populates="owner", cascade="all, delete-orphan")
    # Relationship to Comments
    comments = relationship("Comment", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self): 
        return f"<User {self.username}>"
    



class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(String, nullable=False)  # 'rent' or 'sale'
    price = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    rooms_count = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    total_comments = Column(Integer, nullable=False, server_default="0")

    # Foreign Key to link the user who created the listing
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationship with User model
    owner = relationship("User", back_populates="listings")
    # Relationship with Comment model
    comments = relationship("Comment", back_populates="listing", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Listing {self.address} - {self.type} - {self.price}>"
    
    
    
class Comment(Base): 
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationship with User model
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="comments")
    # Relationship with Listing model
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    listing = relationship("Listing", back_populates="comments") 
    
    def __repr__(self):
        return f"<Comment {self.content[:20]}...>"

    



