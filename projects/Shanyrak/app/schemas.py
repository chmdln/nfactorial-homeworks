from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List 
from datetime import datetime 
import re



class Token(BaseModel):
    access_token: str
    token_type: str

class UserSignupRequest(BaseModel): 
    username: EmailStr 
    password: str 
    name: str 
    phone: str 
    city: str 

    class Config: 
        from_attributes = True

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class UserSignupResponse(BaseModel):
    id: int
    username: str
    name: str
    phone: str
    city: str
    class Config: 
        from_attributes = True


class UserUpdateRequest(BaseModel):
    username: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    class Config: 
        from_attributes = True

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class UserUpdateResponse(BaseModel):
    id: int
    username: str
    name: str
    phone: str
    city: str

    class Config: 
        from_attributes = True



class UserGetResponse(BaseModel):
    id: int
    username: str
    phone: str
    name: str
    city: str

    class Config: 
        from_attributes = True


class ListingPostRequest(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str    

    class Config: 
        from_attributes = True


class ListingPostResponse(BaseModel):
    id: int
    class Config: 
        from_attributes = True


class ListingGetResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int
    total_comments: int
    class Config: 
        from_attributes = True 


class ListingUpdateRequest(BaseModel):
    type: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None
    area: Optional[float] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None
    class Config: 
        from_attributes = True


class ListingUpdateResponse(ListingGetResponse):
    class Config: 
        from_attributes = True


class CommentPostRequest(BaseModel):
    content: str
    class Config:     
        from_attributes = True 


class CommentPostResponse(BaseModel):
    id: int
    content: str 
    user_id: int
    listing_id: int
    class Config: 
        from_attributes = True


class CommentGetResponse(BaseModel):
    id: int
    content: str 
    user_id: int
    created_at: datetime
    class Config: 
        from_attributes = True 


class CommentsResponse(BaseModel):
    comments: List[CommentGetResponse]


class CommentUpdateRequest(BaseModel):
    content: Optional[str] = None
    class Config: 
        from_attributes = True