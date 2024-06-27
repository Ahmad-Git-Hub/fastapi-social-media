from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
import time
from sqlalchemy.orm import Session
from . import models, schemas, variables, utilities
from .database import engine, get_db
from app.routers import post, user


# Creates the tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
        
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "FastApi is here!"}


       
     
