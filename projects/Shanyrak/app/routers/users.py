from fastapi import APIRouter, Depends, Form, HTTPException, status, Response 
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.models import User
from app.database.database import get_db
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from app.schemas import UserSignupRequest, Token, UserUpdateRequest, UserGetResponse
from app.utils import hash, verify_password



router = APIRouter(tags=["Users"])


@router.post("/auth/users", status_code=status.HTTP_200_OK, response_class=Response)
def user_signup(user: UserSignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User with this username already exists"
        )
    
    hashed_password = hash(user.password)
    data = {**user.dict()}
    data["password"] = hashed_password
    new_user = User(**data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return Response(status_code=status.HTTP_200_OK)



@router.post("/auth/users/login", status_code=status.HTTP_200_OK, response_model=Token)
def user_login(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not verify_password(password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )    

    access_token = create_access_token(
        data={"sub": existing_user.username}, 
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    return {"access_token": access_token, "token_type": "bearer"} 




@router.patch("/auth/users/me", status_code=status.HTTP_200_OK, response_class=Response)
def update_user(
    user: UserUpdateRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):  
    
    data = user.dict(exclude_unset=True) 
    if "password" in data:
        data["password"] = hash(data["password"])  

    for key, value in data.items():
        setattr(current_user, key, value)  
    
    db.commit()
    db.refresh(current_user)
    return Response(status_code=status.HTTP_200_OK)
    

    
@router.get("/auth/users/me", status_code=status.HTTP_200_OK, response_model=UserGetResponse)
def get_user(user: User = Depends(get_current_user)):
    return user 

