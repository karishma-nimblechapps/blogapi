from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LogIn(BaseModel):
    email:str
    password:str

class Tokens(BaseModel):
    access_tokens:str
    token_type:str
    
class BlogInUser(BaseModel):
    title: str
    content: str

class UserBase(BaseModel):
    username:str
    email: str

class UserCreate(BaseModel):
    id:int
    first_name: str
    last_name: str
    status: bool
    username:str
    email:str
    password:str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    status: bool

class UserInDB(UserBase):
    id: int
    first_name: str
    last_name: str
    email: str
    status: bool
    blogs: List[BlogInUser]

class UserInResponse(UserBase):
    id: int
    first_name: str
    last_name: str
    username:Optional[str]
    email: str

    class Config:
        orm_mode = True

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    user_id:int
    title:str
    content:str

class BlogUpdate(BlogBase):
    user_id:int
    title: str
    content: str
    status: Optional[bool]=None

class BlogInDB(BlogBase):
    id: int
    title: str
    content: str
    status: bool
    created_at: datetime
    user_id: int
    is_top:bool

class BlogResponse(BlogBase):
    id: int
    status: bool
    is_top:bool

    class Config:
        orm_mode = True

class BlogUpdateTop(BlogBase):
    top_blog_ids:List[int]

class ToggleUpdate(BaseModel):
   status:bool




    




    




