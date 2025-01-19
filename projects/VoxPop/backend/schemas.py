from pydantic import BaseModel
from typing import List
from datetime import datetime

class Post(BaseModel):
    id: int
    content: str
    category: str 
    likes: int 
    created_at: datetime

class PostCreate(BaseModel):
    content: str 
    category: str 

