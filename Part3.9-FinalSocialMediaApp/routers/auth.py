from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
import models,schemas,utils,database,oauth2
from database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
     tags=['Authentication']
)

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    #once login is successful we can create oauth token
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {"token" : access_token, "token_type" : "bearer" }