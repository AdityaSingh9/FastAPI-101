from fastapi import FastAPI, Path, Query, HTTPException
#path and query helps to validate the path params
from typing import Optional
#pydantics : library for data modeling, data validation , data parsing and efficient error handling
#Field lets you add field level validations
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    '''
    #removing this since it will become class variables this way
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    '''
    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date

#book request will do the validation
class BookRequest(BaseModel):   #Basemodel is the pydantic model which adds more functionality for data validation
    id: Optional[int] = Field(description="Id is not needed on create operation | post request",default=None)    #optional field
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str =  Field(min_length=1,max_length=100)
    rating: int = Field(gt=-1,lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    '''
    current Request body - Schema
    {
        "id": 0,
        "title": "string",
        "author": "string",
        "description": "string",
        "rating": 0,
        "published_date": 0
    }
    model config: below code will help to display default values instead of 0 and string
    '''
    model_config ={
        "json_schema_extra" : {
            "example": {
                
                "title": "My new book",
                "author": "Aditya Singh",
                "description": "Greatest Book of all Time",
                "rating": 3,
                "published_date": 2001
            }
        }     
    }


#creating sample BOOKS 
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

#function to find book id for the new post request!
def find_book_id(book : Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
    # above is alternative way to code the same as below using ternary operator
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    # return book

#get all books:
@app.get("/books",status_code=status.HTTP_200_OK)   #explicitly defining the status codes
async def read_all_books():
    return BOOKS 

#fetch sinle book by book_id: using uri param
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id : int = Path(gt=0)):  #path param validation - book_id >0
    for book in BOOKS:
        if book.id==book_id:
            return book
    #handling case: book not found (404 exception)
    raise HTTPException(status_code=404, detail="Item not found")
              
#fetch single book by rating: using query params
@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_ratings(book_rating : int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

#read books by publish date: using query params
@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date : int  = Query(gt=1999,lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date==publish_date:
            books_to_return.append(book)
    return books_to_return

#create book:
@app.post("/books/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):   #validating that the item matches BookRequest 
    #if we append book_request directly we will have two different kinds of object in list (Books and BookRequest type)
    new_book= Book(**book_request.model_dump())     #**book_request.model_dump() - converting the request to Book object, .dict() is deprecated
    BOOKS.append(find_book_id(new_book))    #instead of adding any random id which comes from the request, its better to assign it using a function by checking the last inserted value!

#update book : PUT operation
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed=True   
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not found")
    
    
#delete book : DELETE Operation
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int = Path(gt=0)):
    book_deleted=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            book_deleted=True
            break
    if not book_deleted:
        raise HTTPException(status_code=404,detail="Item not found")