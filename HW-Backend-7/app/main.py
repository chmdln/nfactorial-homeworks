from fastapi import (
    Cookie, FastAPI, Form, File, 
    UploadFile, Request, Response,
    templating, HTTPException, status,
    Depends
)

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import timedelta
from typing import Optional
import uuid
import json

from app.auth import create_access_token, verify_access_token
from app.repository.flowers import FlowersRepository
from app.repository.purchases import PurchasesRepository
from app.repository.users import UsersRepository
from app.utils import json_validator
from . import schemas 
from .auth import oauth2_scheme


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = templating.Jinja2Templates("templates")

flowers_repo = FlowersRepository()
purchases_repo= PurchasesRepository()
users_repo = UsersRepository()




@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup")
def render_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", status_code=status.HTTP_200_OK)
def user_signup(
    request: schemas.UserSignupRequest
):
    email = request.email
    full_name = request.full_name
    password = request.password
    user = users_repo.create_user(email, full_name, password)

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
    profile_photo: Optional[UploadFile] = File(None) 
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
        users_repo.save_profile_photo(user_id, {"profile_photo": file_path})
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
):
    user = users_repo.get_user_by_email(username)
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail=f"User with username {username} does not exist."
        )
    if user.password != password:
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
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )    
    
    payload = verify_access_token(access_token)
    user_id = uuid.UUID(payload["sub"])
    user = users_repo.get_user_by_id(user_id)

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
def render_flowers_form(request: Request):
    return templates.TemplateResponse("flowers.html", {
        "request": request,
        "flowers": flowers_repo.flowers
    })


@app.post("/flowers", 
          status_code=status.HTTP_201_CREATED, 
          response_model=schemas.AddFlowerResponse
)  
def add_flower(
    request: Request,
    data: schemas.AddFlowerRequest
):
    name = data.name
    cost = data.cost
    count = data.count

    flower = flowers_repo.add_flower(name, cost, count)

    if isinstance(flower, dict): 
        if "error" in flower and flower["error"] == "Flower already exists":
            raise HTTPException(
                status_code=409, 
                detail=f"Flower with name {name} already exists."
            )
    return flower 



@app.post("/cart/items")
def add_flower_to_cart(
    flower_id: str = Form(...),
    quantity: str = Form(default="1"),
    cart: str = Cookie(default="[]"),
):  
    
    cart_json = json.loads(cart)
    quantity = int(quantity)
    flower_id = uuid.UUID(flower_id)
    flower = flowers_repo.get_flower_by_id(flower_id)
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
    
    cart_json.append(
        {
            "flower_id": str(flower_id), 
            "quantity": str(quantity)
         }
    )

    updated_cart = json.dumps(cart_json)
    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(key="cart", value=updated_cart)
    return response



@app.get("/cart/items", 
         status_code=status.HTTP_200_OK, 
         response_model=list[schemas.AddToCartResponse]
)
def render_cart(
    request: Request,
    cart: str = Cookie(default="[]"),
):
    
    cart_json = json_validator(cart)
    cart_items, total_cost = [], 0 

    for cart_item in cart_json:
        flower_id = uuid.UUID(cart_item["flower_id"])
        quantity = int(cart_item["quantity"])

        flower = flowers_repo.get_flower_by_id(flower_id)
        if flower is None: 
            raise HTTPException(
                status_code=404, 
                detail=f"Flower with id {flower_id} not found."
            )

        cart_items.append(schemas.AddToCartResponse(
            id=flower_id,
            name=flower.name,
            cost=flower.cost,
            quantity=quantity,
            total_cost=round(flower.cost * quantity, 2)
        ))
    return cart_items  



@app.post("/purchased", status_code=status.HTTP_200_OK)
def save_user_purchase(
    request: Request,
    cart: str = Cookie(default="[]"),
    access_token: str = Depends(oauth2_scheme)
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )
    
    payload = verify_access_token(access_token)
    user_id = uuid.UUID(payload["sub"])
    user = users_repo.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )

    cart = json.loads(cart)
    for cart_item in cart:
        flower_id = uuid.UUID(cart_item["flower_id"])
        flower = flowers_repo.get_flower_by_id(flower_id)
        if flower is None: 
            raise HTTPException(
                status_code=404, 
                detail=f"Flower with id {flower_id} not found."
            )
        
        cart_item.update(
            {
                "name": flower.name, 
                "cost": flower.cost
            }
        )
    purchases_repo.save_purchase(user_id, cart)
    return Response(status_code=status.HTTP_200_OK)



@app.get("/purchased", 
         status_code=status.HTTP_200_OK, 
         response_model=list[schemas.UserPurchaseResponse]
)
def render_user_purchase(
    request: Request,
    access_token: str = Depends(oauth2_scheme)
):
    if access_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized."
        )
    
    payload = verify_access_token(access_token)
    user_id = uuid.UUID(payload["sub"])
    user = users_repo.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )
    
    user_purchases = purchases_repo.get_purchase(user_id)
    return user_purchases


@app.post("/logout")
def logout(response: Response) -> Response:
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="cart")
    return response 







