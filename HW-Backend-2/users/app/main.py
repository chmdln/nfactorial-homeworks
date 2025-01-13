from fastapi import FastAPI, Request, Response, Query
from fastapi.templating import Jinja2Templates

from .users import create_users

users = create_users(100)  # Здесь хранятся список пользователей
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/users")
def get_users(request: Request, page: int = Query(1, gt=0), limit: int = Query(len(users), gt=0)):
    start = (page - 1) * limit
    end = start + limit
    
    return templates.TemplateResponse("/users/index.html", 
    {   
        "request": request, 
        "users": users[start:end]
    })



@app.get("/users/{id}")
def get_user(request: Request, id: int):
    for user in users: 
        if user["id"] == id:
            return templates.TemplateResponse("/users/user.html", 
                {   
                    "request": request, 
                    "user": user
                })
    return Response(status_code=404, content="Not found")


