from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
''' create a class to define the schema for validation,should extend basemodel '''
# class PostWithValidation(BaseModel):     
#     title: str
    # content: str
    # published: bool = True

#creating new class with inheritance for schema validation in different cases like create and update
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

#response
class PostResponse(PostBase):
    id: int
    created_at: datetime 
    class Config:
        #orm_mode = True
        from_attributes: True

#users schema:
class UserCreate(BaseModel):
    email : EmailStr 
    password : str 

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at: datetime 
    class Config:
        #orm_mode = True
        from_attributes: True

class UserLogin(BaseModel):
    email : EmailStr
    password : str 
    class Config:
        #orm_mode = True
        from_attributes: True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    
    