from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.routers import users, posts, chat 
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(chat.router)

app.mount("/app/media", StaticFiles(directory="app/media/"), name="media")

Base.metadata.create_all(bind=engine)


