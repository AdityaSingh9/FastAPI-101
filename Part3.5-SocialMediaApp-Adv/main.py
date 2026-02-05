
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel  #pydantic is a separate model , not a part of fastAPI but can be used for various things like schema validation
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional
from random import randrange
# importing from other two files 
from sqlalchemy.orm import Session
import models
from database import engine , get_db

models.Base.metadata.create_all(bind=engine)    #this craetes the table

app = FastAPI()     #creates/initializes object of FastAPI class 


#connecting to DB
while True:
    try:
        #DON'T HARDCODE IN REAL TIME
        conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='Aditya988@',cursor_factory=RealDictCursor)
        cursor = conn.cursor()  # exectute the queries using 'cursor' after connecting to the db using 'conn'
        print("Database connection was succesfull!")
        break
    except Exception as error:      #raise exception in case of error
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)       #wait for  2 sec before retry

# building a validation to follow the schema : Using pydentic basemodel
''' create a class to define the schema for validation,should extend basemodel '''
class PostWithValidation(BaseModel):     
    title: str
    content: str
    published: bool = True

#test endpoint
@app.get("/test")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()    
    return {"data" : posts}

@app.get("/")   #This is a decorator, When a client sends an HTTP GET request to the root URL /,it calls the function below."
def root(): #this is the normal function which defines the behaviour 
    return {"message": "Hello Aditya, Social Media app is Up and Running Fine!"}

# performing CRUD on postgress DB

#get all posts: 1
@app.get("/posts",status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""   select * from posts   """) #this executes but doesnt return anything so we need to fetch it!
    # posts = cursor.fetchall()    #fetching results of above query
    posts = db.query(models.Post).all()   
    return {"data" : posts}

#create a new post: 2
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_new_post(payload : PostWithValidation ,db: Session = Depends(get_db)):      
    # (%s part saves from sql injection : make sure there is no weird sql commands being passed)
    # cursor.execute("""Insert into posts (title,content,published) values (%s,%s,%s) returning *""",(payload.title,payload.content,payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()   #commit changes from stage
    
    #alternative way of this:
    # new_post=models.Post(title=payload.title, content=payload.content, published=payload.published)
    new_post=models.Post(**payload.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    #returns the content
    return {"data": new_post }
    
#get posts by id: 3
''' implementing same method but in an alternative way'''
@app.get("/posts/{id}",status_code=status.HTTP_200_OK)  
def get_post(id : int, response : Response,db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where id = %s """,(str(id)))
    # get_post = cursor.fetchone()
    # print(get_post)
    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    return {"post_detail" : post}

#delete post by id: 4
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    post.delete(synchronize_session=False)
    db.commit()

    return 

#update post by id: 5
@app.put("/posts/{id}")
def update_post(id: int,payload: PostWithValidation,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s returning *""", (payload.title,payload.content,payload.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    post_query.update(payload.model_dump(),synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

