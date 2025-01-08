from fastapi import FastAPI
import math

app = FastAPI()

# 3. fastapi-hello
@app.get("/")
async def root():
    return {"message": "Hello, nfactorial!"} 


# 4. fastapi-meaning-life
@app.post("/meaning-of-life")
async def meaning():
    return {"meaning": "42"} 


# 5. fastapi-nfactorial
@app.get("/{num}")
async def factorial(num: int):
    res = math.factorial(num)
    return {"nfactorial": res}