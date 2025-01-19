import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models 
from .routers import posts


app = FastAPI()
app.include_router(posts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

models.Base.metadata.create_all(bind=engine)

# if __name__ == "__main__": 
#     uvicorn.run(app, host="localhost", port=8000) 