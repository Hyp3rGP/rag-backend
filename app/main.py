from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user
from app.api import admin
from app.db import database  # connect to db


app = FastAPI(
    title="RAG Model API",
    description="API for the RAG model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"msg": "Welcome to the RAG model API!"}
