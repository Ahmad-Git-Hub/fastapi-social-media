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
# while True:
#         try:
#              conn = psycopg.connect(host=variables.host, dbname=variables.dbname,
#                                     user=variables.user, password=variables.passowrd)
#              cursor = conn.cursor()
#              print("Databse connection is succussfull!")
#              break
        
#         except Exception as error:
#             print(error)
#             time.sleep(5)


        
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "FastApi is here!"}


       
     
