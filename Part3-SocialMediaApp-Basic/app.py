
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel  #pydantic is a separate model , not a part of fastAPI but can be used for various things like schema validation
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional
from random import randrange

app = FastAPI()     #creates/initializes object of FastAPI class 

#connecting to DB
while True:
    try:
        #DON'T HARDCODE IN REAL TIME
        conn = psycopg2.connect(host='HOSTNAME',database='DBNAME',user='USERNAME',password='PASSWORD',cursor_factory=RealDictCursor)
        cursor = conn.cursor()  # exectute the queries using 'cursor' after connecting to the db using 'conn'
        print("Database connection was succesfull!")
        break
    except Exception as error:      #raise exception in case of error
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)       #wait for 2 sec before retry

# building a validation to follow the schema : Using pydentic basemodel
''' create a class to define the schema for validation,should extend basemodel '''
class PostWithValidation(BaseModel):     
    title: str
    content: str
    published: bool = True

@app.get("/")   #This is a decorator, When a client sends an HTTP GET request to the root URL /,it calls the function below."
def root(): #this is the normal function which defines the behaviour 
    return {"message": "Hello Aditya, Social Media app is Up and Running Fine!"}

# performing CRUD on postgress DB

#get all posts: 1
@app.get("/posts",status_code=status.HTTP_200_OK)
def get_all_posts():
    cursor.execute("""   select * from posts   """) #this executes but doesnt return anything so we need to fetch it!
    posts = cursor.fetchall()    #fetching results of above query
    return {"data" : posts}

#create a new post: 2
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_new_post(payload : PostWithValidation):      #does the schema part 
    # (%s part saves from sql injection : make sure there is no weird sql commands being passed)
    cursor.execute("""Insert into posts (title,content,published) values (%s,%s,%s) returning *""",(payload.title,payload.content,payload.published))
    new_post = cursor.fetchone()
    conn.commit()   #commit changes from stage
    return {"data": new_post }
    
#get posts by id: 3
''' implementing same method but in an alternative way'''
@app.get("/posts/{id}",status_code=status.HTTP_200_OK)  
def get_post(id : int, response : Response):
    cursor.execute("""select * from posts where id = %s """,(str(id)))
    get_post = cursor.fetchone()
    print(get_post)
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    return {"post_detail" : get_post}

#delete post by id: 4
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    return {"data": deleted_post }

#update post by id: 5
@app.put("/posts/{id}")
def update_post(id: int,payload: PostWithValidation):
    cursor.execute("""UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s returning *""", (payload.title,payload.content,payload.published,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    return {"data": updated_post }

