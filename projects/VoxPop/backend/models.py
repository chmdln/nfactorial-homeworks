from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.sql import func
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DATETIME,
        default=func.now(),
        nullable=False
    )
    class Config:
        orm_mode = True 


