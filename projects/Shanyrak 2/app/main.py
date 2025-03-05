from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.routers import users, listings



app = FastAPI()
app.include_router(users.router)
app.include_router(listings.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


Base.metadata.create_all(bind=engine)



    





    

    

    