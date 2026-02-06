from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
import models,schemas,utils
from database import get_db

router = APIRouter(
     tags=['Users']
)

"""  Users Implementations """
#craete users
@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_new_user(payload : schemas.UserCreate ,db: Session = Depends(get_db)):      

    #hash the passwords - payload.password
    payload.password = utils.hash(payload.password)

    new_user=models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    #returns the content
    return new_user 

@router.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with id:  {id} doesnt exist")
    return user
