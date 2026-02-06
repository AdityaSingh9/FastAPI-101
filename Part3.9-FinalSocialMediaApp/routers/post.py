from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
import models,schemas,utils,oauth2
from database import get_db
from typing import List

router = APIRouter(
    tags=['Posts']
)


# performing CRUD on postgress DB
#get all posts: 1
@router.get("/posts",status_code=status.HTTP_200_OK,response_model= List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()   
    return  posts

#create a new post: 2
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_new_post(payload : schemas.PostCreate ,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):      
    print(user_id)
    new_post=models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    #returns the content
    return new_post 
    
#get posts by id: 3
''' implementing same method but in an alternative way'''
@router.get("/posts/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)  
def get_post(id : int, response : Response,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    return post

#delete post by id: 4
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    post.delete(synchronize_session=False)
    db.commit()
    return 

#update post by id: 5
@router.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id: int,payload: schemas.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnt exist")
    post_query.update(payload.model_dump(),synchronize_session=False)
    db.commit()
    return  post_query.first()