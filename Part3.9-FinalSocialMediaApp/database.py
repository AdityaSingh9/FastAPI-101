#database.py will have db connection details
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#dont hardcode in real time
SQLALCHEMY_DATABASE_URL = 'postgresql://username:password@hostNameOrIPaddress/DBname' 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

#yield allows a function to return a value temporarily, pause execution, and resume later, which is perfect for managing resources like database connections.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()