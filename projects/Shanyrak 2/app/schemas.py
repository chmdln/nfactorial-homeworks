from pydantic import BaseModel, EmailStr, field_validator
from fastapi.params import Query
from typing import Optional, List, Annotated
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


class ListingValidator(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str    

    # Ensure 'type' is either 'sell' or 'rent'
    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        if value not in {"sell", "rent"}:
            raise ValueError("Invalid type. Must be 'sell' or 'rent'.")
        return value

    # Ensure 'price' is a non-negative integer
    @field_validator("price")
    @classmethod
    def validate_price(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Price must be a non-negative value.")
        return value

    # Ensure 'area' is a positive float
    @field_validator("area")
    @classmethod
    def validate_area(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Area must be a positive number.")
        return value

    # Ensure 'rooms_count' is at least 1
    @field_validator("rooms_count")
    @classmethod
    def validate_rooms_count(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Rooms count must be at least 1.")
        return value

    # Ensure 'address' and 'description' are not empty
    @field_validator("address", "description")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be empty.")
        return value



class ListingPostRequest(ListingValidator):
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


class ListingUpdateRequest(ListingValidator):
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



class FavoriteListingResponse(BaseModel):
    id: int
    address: str 
    class config: 
        from_attributes = True


class FavoriteListingsResponse(BaseModel):
    shanyraks: List[FavoriteListingResponse]
    class Config: 
        from_attributes = True
    


class ListingFilter(BaseModel):
    limit: Annotated[int, Query(ge=1)] = 10
    offset: Annotated[int, Query(ge=0)] = 0 
    type: Annotated[str | None, Query()] = None
    rooms_count: Annotated[int | None, Query(ge=1)] = None
    price_from: Annotated[int | None, Query(ge=0)] = None
    price_until: Annotated[int | None, Query(ge=0)] = None

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, value):
        """Ensures limit is between 1 and 100 (reasonable pagination range)."""
        if value < 1:
            raise ValueError("limit must greater than 0.")
        return value

    @field_validator("offset")
    @classmethod
    def validate_offset(cls, value):
        """Ensures offset is at least 0 (can't be negative)."""
        if value < 0:
            raise ValueError("offset must be at least 0.")
        return value
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        """Ensures type is either 'sell' or 'rent'."""
        if value is not None and value not in {"sell", "rent"}:
            raise ValueError("Invalid type. Must be 'sell' or 'rent'.")
        return value

    @field_validator("rooms_count")
    @classmethod
    def validate_rooms_count(cls, value):
        """Ensures rooms_count is at least 1."""
        if value is not None and value < 1:
            raise ValueError("rooms_count must be at least 1.")
        return value

    @field_validator("price_from", "price_until")
    @classmethod
    def validate_price(cls, value):
        """Ensures price_from and price_until are non-negative."""
        if value is not None and value < 0:
            raise ValueError("Price must be a non-negative value.")
        return value

    @field_validator("price_until")
    @classmethod
    def validate_price_range(cls, value, info):
        """Ensures price_from is not greater than price_until."""
        price_from = info.data.get("price_from")
        if price_from is not None and value is not None and price_from > value:
            raise ValueError("price_from must be less than or equal to price_until.")
        return value

    

class ListingGetAllResponse(BaseModel):
        id: int 
        type: str 
        price: int
        address: str
        area: float
        rooms_count: int 

        class Config:
            from_attributes = True

class ListingsGetAllResponse(BaseModel):
    total: int 
    listings: List[ListingGetAllResponse]
    class Config: 
        from_attributes = True
    


