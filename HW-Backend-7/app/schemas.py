from pydantic import BaseModel, EmailStr, field_validator
import re 
import uuid 


class UserSignupRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str

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
    

class AddFlowerRequest(BaseModel):
    name: str
    cost: float
    count: int

    class Config:
        from_attributes = True


class AddFlowerResponse(BaseModel):
    id: uuid.UUID

    class Config:
        from_attributes = True


class AddToCartResponse(BaseModel):
    id: uuid.UUID
    name: str
    cost: float
    quantity: int
    total_cost: float

    class Config:
        from_attributes = True


class UserPurchaseResponse(BaseModel):
    user_id: uuid.UUID
    flower_id: uuid.UUID
    name: str
    cost: float
    quantity: int

    class Config:
        from_attributes = True
