from pydantic import BaseModel 
from datetime import datetime
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str 

class User(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool
    is_profile_complete: bool
    created_at: datetime 

    class Config:
        from_attributes=True

    

class UserCreateRequest(BaseModel):
    email: str  
    password: str 

class UserCreateResponse(Token):
    pass 


class UserPersonalizeProfileRequest(BaseModel):
    first_name: str
    last_name: str
    company: str
    position: str
    location: str

class UserPersonalizeProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    company: str
    position: str
    location: str
    email: str
    is_verified: bool
    is_profile_complete: bool
    created_at: datetime 

class UserLoginRequest(BaseModel):
    email: str 
    password: str 

class UserLoginResponse(Token):
    pass

class UserGetResponse(User):
    pass

class UserResetPasswordCodeRequest(BaseModel):
    email: str

class UserResetPasswordRequest(BaseModel):
    code: str
    password: str


class Like(BaseModel):
    id: str
    user_id: str
    post_id: str

class Comment(BaseModel):
    id: str
    content: str
    user_id: str
    post_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: User

class Post(BaseModel):
    id: str
    content: str
    media_url: Optional[str] = None
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: List[Like] = []
    comments: List[Comment] = []

class PostCreateResponse(Post): 
    user: User              

class PostEditResponse(Post):
    user: User             

class PostLikeResponse(Post):
    user: User 

class PostUnlikeResponse(PostLikeResponse):
    pass 

class PostCommentResponse(Post):
    user: User 

class PostCommentRequest(BaseModel):
    content: str

class EditPostCommentRequest(PostCommentRequest):
    pass 

class EditPostCommentResponse(PostCommentRequest):
    pass 


class UserBase(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    company: str
    position: str
    location: str
    is_verified: bool
    is_profile_complete: bool
    created_at: datetime

    class Config:
        from_attributes=True 

class GetConnectionResponse(BaseModel):
    author_id: str 
    sender: UserBase 
    recipient: UserBase 

    class Config:
        from_attributes=True


class CreateConversationRequest(BaseModel):
    recipent_id: str
    content: str 
