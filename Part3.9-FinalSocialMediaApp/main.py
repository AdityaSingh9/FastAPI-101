
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel  #pydantic is a separate model , not a part of fastAPI but can be used for various things like schema validation
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional, List
from random import randrange
from sqlalchemy.orm import Session
import models,schemas,utils
from database import engine , get_db
from routers import post, user,auth

#13679804072024
models.Base.metadata.create_all(bind=engine)    #this craetes the table

app = FastAPI()     #creates/initializes object of FastAPI class 

#connecting to DB
while True:
    try:
        #DON'T HARDCODE IN REAL TIME
        conn = psycopg2.connect(host='YOUR_HOST',database='YOUR_DB',user='USER',password='PASSWORD',cursor_factory=RealDictCursor)
        cursor = conn.cursor()  # exectute the queries using 'cursor' after connecting to the db using 'conn'
        print("Database connection was succesfull!")
        break
    except Exception as error:      #raise exception in case of error
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)       #wait for  2 sec before retry


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")   #This is a decorator, When a client sends an HTTP GET request to the root URL /,it calls the function below."
def root(): #this is the normal function which defines the behaviour 
    return {"message": "Hello, Social Media app is Up and Running Fine!"}

