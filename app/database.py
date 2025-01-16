from sqlalchemy import create_engine,Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from fastapi import Depends

hostname='localhost'
database='blogfinal'
username='postgres'
pwd='nimble123'
port_id=5432

Base=declarative_base()

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String,index=True)
    last_name=Column(String,index=True)
    email=Column(String,unique=True,index=True)
    status=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    username=Column(String,unique=True)
    hashed_password=Column(String,nullable=True)
    blogs=relationship("Blog",back_populates="user")

class Blog(Base):
    __tablename__="blogs"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    title=Column(String,index=True,unique=True)
    content=Column(String)
    status=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    is_top=Column(Boolean,default=True)
    user=relationship("User",back_populates="blogs")

engine=create_engine(f'postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}')
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
    
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


    

         
       





   