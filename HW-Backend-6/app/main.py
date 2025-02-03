from fastapi import Cookie, FastAPI, Form, File, UploadFile, Request, Response, templating, HTTPException
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


@app.post("/signup")
def user_signup(
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    profile_photo: Optional[UploadFile] = File(None)
):
    if profile_photo and profile_photo.filename: 
        if profile_photo.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, 
                detail="Invalid image format. Only JPEG and PNG are supported."
            )
    
    user = users_repo.create_user(email, full_name, password)

    if isinstance(user, dict):
        if "error" in user and user["error"] == "Email already exists":
            raise HTTPException(
                status_code=409, 
                detail=f"User with email {email} already exists."
            )
    
    if profile_photo and profile_photo.filename: 
        unique_filename = f"{uuid.uuid4()}_{profile_photo.filename}"
        file_path = f"static/uploads/{unique_filename}"
        with open(file_path, "wb") as f:
            f.write(profile_photo.file.read())

        users_repo.save_profile_photo(user.id, {"profile_photo": file_path})

    response = RedirectResponse(url="/login", status_code=303)
    return response


@app.get("/login")
def render_login_form(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })


@app.post("/login")
def user_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    user = users_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail=f"User with email {email} does not exist."
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
    
    response = RedirectResponse(url="/profile", status_code=303)  
    response.set_cookie(key="access_token", value=access_token)  
    return response
    


@app.get("/profile")
def render_user_profile(
    request: Request,
    access_token: str = Cookie(None),
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

@app.post("/flowers")  
def add_flower(
    request: Request,
    name: str = Form(...),
    cost: float = Form(...),
    count: int = Form(...)
):
    flower = flowers_repo.add_flower(name, cost, count)

    if isinstance(flower, dict): 
        if "error" in flower and flower["error"] == "Flower already exists":
            raise HTTPException(
                status_code=409, 
                detail=f"Flower with name {name} already exists."
            )
    response = RedirectResponse(url="/flowers", status_code=303)
    return response 



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
    response = RedirectResponse(url="/flowers", status_code=303)
    response.set_cookie(key="cart", value=updated_cart)
    return response



@app.get("/cart/items")
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
        flower.quantity = quantity
        cart_items.append(flower)
        total_cost += (flower.cost*quantity)
    total_cost = round(total_cost, 2)

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart": cart_items,
        "total_cost": total_cost
    })


@app.post("/purchased")
def save_user_purchase(
    request: Request,
    cart: str = Cookie(default="[]"),
    access_token: str = Cookie(None),
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
    return RedirectResponse(url="/purchased", status_code=303) 



@app.get("/purchased")
def render_user_purchase(
    request: Request,
    access_token: str = Cookie(None),
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
    return templates.TemplateResponse("purchased.html", 
        {
            "request": request, 
            "purchases": user_purchases
        }
    )


@app.post("/logout")
def logout(response: Response) -> Response:
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="cart")
    return response 













