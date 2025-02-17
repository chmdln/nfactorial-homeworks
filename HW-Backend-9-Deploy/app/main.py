from fastapi import (
    FastAPI, Form, File, 
    UploadFile, Request, Response,
    templating, HTTPException, status,
    Depends
)

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
import uuid

from app.auth import create_access_token, verify_access_token
from app.database.repository.flowers import FlowersRepository, FlowerCreate, FlowerUpdate 
from app.database.repository.purchases import PurchasesRepository
from app.database.repository.users import UsersRepository, UserCreate 
from app.database.repository.carts import CartsRepository, AddToCart
from app.database.database import get_db
from app.utils import verify
from . import schemas 
from .auth import oauth2_scheme



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = templating.Jinja2Templates("templates")

flowers_repo = FlowersRepository()
purchases_repo= PurchasesRepository()
users_repo = UsersRepository()
carts_repo = CartsRepository()




@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup")
def render_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", status_code=status.HTTP_200_OK)
def user_signup(
    request: schemas.UserSignupRequest, 
    db: Session = Depends(get_db),
):
    email = request.email
    full_name = request.full_name
    password = request.password
    user = users_repo.create_user(db, 
        UserCreate(
            email=email,
            full_name=full_name,
            password=password
        ))

    if isinstance(user, dict):
        if "error" in user and user["error"] == "Email already exists":
            raise HTTPException(
                status_code=409, 
                detail=f"User with email {email} already exists."
            )
    return Response(status_code=status.HTTP_200_OK)




@app.post("/upload_profile_photo/{user_id}", 
          status_code=status.HTTP_201_CREATED,
)
def user_profile_photo(
    user_id: str,
    profile_photo: Optional[UploadFile] = File(None), 
    db: Session = Depends(get_db),
):
    if profile_photo and profile_photo.filename: 
        if profile_photo.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, 
                detail="Invalid image format. Only JPEG and PNG are supported."
            )
        
        unique_filename = f"{uuid.uuid4()}_{profile_photo.filename}"
        file_path = f"static/uploads/{unique_filename}"
        with open(file_path, "wb") as f:
            f.write(profile_photo.file.read())
        users_repo.save_profile_photo(db, user_id, {"profile_photo": file_path})
    return Response(status_code=status.HTTP_201_CREATED)



@app.get("/login")
def render_login_form(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })


@app.post("/login")
def user_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = users_repo.get_user_by_email(db, username)
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail=f"User with username {username} does not exist."
        )
    
    if not verify(password, user.password): 
        raise HTTPException(
            status_code=401, 
            detail=f"Password is incorrect."        
        )    
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=timedelta()
    ) 
    return {"access_token": access_token, "token_type": "bearer"}
    


@app.get("/profile")
def render_user_profile(
    request: Request,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )    
    
    payload = verify_access_token(access_token)
    user_id = payload["sub"]
    user = users_repo.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )
    
    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user
    })



@app.get("/flowers")
def render_flowers_form(request: Request, db: Session = Depends(get_db)):
    flowers = flowers_repo.get_all_flowers(db)
    return templates.TemplateResponse("flowers.html", {
        "request": request,
        "flowers": flowers 
    })



@app.post("/flowers", 
          status_code=status.HTTP_201_CREATED, 
          response_model=schemas.AddFlowerResponse
)  
def add_flower(
    data: schemas.AddFlowerRequest, 
    db: Session = Depends(get_db),
):
    name = data.name
    cost = data.cost
    count = data.count

    flower = flowers_repo.add_flower(db, FlowerCreate(name=name, cost=cost, count=count))

    if isinstance(flower, dict): 
        if "error" in flower and flower["error"] == "Flower already exists":
            raise HTTPException(
                status_code=409, 
                detail=f"Flower with name {name} already exists."
            )
    return flower 



@app.patch("/flowers/{flower_id}", 
           status_code=status.HTTP_200_OK, 
           response_model=schemas.UpdateFlowerResponse)
def update_flower(
    flower_id: str,
    data: schemas.UpdateFlowerRequest,
    db: Session = Depends(get_db),
):
    name = data.name
    cost = data.cost
    count = data.count

    flower = flowers_repo.update_flower(db, flower_id, FlowerUpdate(name=name, cost=cost, count=count))

    if isinstance(flower, dict): 
        if "error" in flower and flower["error"] == "Flower not found":
            raise HTTPException(
                status_code=404, 
                detail=f"Flower with id {flower_id} not found."
            )
    return flower   



@app.delete("/flowers/{flower_id}", 
            status_code=status.HTTP_204_NO_CONTENT)
def delete_flower(flower_id: str, db: Session = Depends(get_db)):
    flower = flowers_repo.get_flower_by_id(db, flower_id)
    if not flower:
        raise HTTPException(
            status_code=404, 
            detail=f"Flower with id {flower_id} not found."
        )
    flowers_repo.delete_flower(db, flower_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.post("/cart/items", status_code=status.HTTP_200_OK)
def add_flower_to_cart(
    user_id: str, 
    flower_id: str = Form(...),
    quantity: str = Form(default="1"),
    db: Session = Depends(get_db)
):  
    
    quantity = int(quantity)
    flower = flowers_repo.get_flower_by_id(db, flower_id)
    
    if flower is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Flower with id {flower_id} not found."
        )
    
    if quantity > flower.count:
        raise HTTPException(
            status_code=400, 
            detail="Invalid quantity."
        )
    
    carts_repo.add_to_cart(db, 
        AddToCart(
            user_id=user_id,
            flower_id=flower_id,
            quantity=quantity
        ) 
    )
    return Response(status_code=status.HTTP_200_OK)

 

@app.get("/cart/items", 
         status_code=status.HTTP_200_OK, 
         response_model=schemas.AddToCartResponse
)
def render_cart(
    user_id: str,
    db: Session = Depends(get_db)
):
    
    cart_db = carts_repo.get_cart(db, user_id)
    if not cart_db:
        raise HTTPException(
            status_code=404, 
            detail="Cart not found."
        )
    
    cart_items = []
    total_cost = 0 

    for cart_item in cart_db.items:
        flower_id = cart_item.flower_id
        quantity = int(cart_item.quantity)

        flower = flowers_repo.get_flower_by_id(db, flower_id)
        if flower is None: 
            raise HTTPException(
                status_code=404, 
                detail=f"Flower with id {flower_id} not found."
            )

        total_cost += (flower.cost * quantity)
        cart_items.append(schemas.AddToCartItem(
            id=flower_id,
            name=flower.name,
            cost=flower.cost,
            quantity=quantity,
        ))

    return {
        "items": cart_items, 
        "total_cost": round(total_cost, 2)
    }



@app.post("/purchased", status_code=status.HTTP_200_OK)
def save_user_purchase(
    access_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )
    
    payload = verify_access_token(access_token)
    user_id = payload["sub"]
    user = users_repo.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )

    cart = carts_repo.get_cart(db, user_id)
    for cart_item in cart.items:
        flower_id = cart_item.flower_id
        flower = flowers_repo.get_flower_by_id(db, flower_id)
        if flower is None: 
            raise HTTPException(
                status_code=404, 
                detail=f"Flower with id {flower_id} not found."
            )
        
        cart_item.name = flower.name
        cart_item.cost = flower.cost
    purchases_repo.save_purchase(db, user_id, cart)
    return Response(status_code=status.HTTP_200_OK)



@app.get("/purchased", 
         status_code=status.HTTP_200_OK, 
         response_model=list[schemas.UserPurchaseResponse]
)
def render_user_purchase(
    access_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )
    
    payload = verify_access_token(access_token)
    user_id = payload["sub"]
    user = users_repo.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )
    
    user_purchases = purchases_repo.get_purchase(db, user_id)
    return user_purchases


@app.post("/logout")
def logout(response: Response) -> Response:
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="cart")
    return response 







