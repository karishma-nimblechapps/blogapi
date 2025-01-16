from typing import Annotated
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db,User
from app.schemas import Tokens,LogIn,UserCreate,UserInResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2AuthorizationCodeBearer

SECRET_KEY = "320560" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2AuthorizationCodeBearer(tokenUrl='auth/token',authorizationUrl='auth/authorize')

router=APIRouter()

async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password) 

async def get_password_hash(password: str):
    return pwd_context.hash(password) 

async def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta 
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get("sub")
        user_id:int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401,detail="unauthorized user")
        return{"username":username,"id":user_id}
    except InvalidTokenError:
        raise HTTPException(status_code=401,detail="not a validate user")

#API Endpoints
@router.post("/signup",response_model=UserInResponse)
async def signup(user:UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="email already registered")
    
    hashed_password = await get_password_hash(user.password)

    db_user=User(id=user.id,first_name=user.first_name,last_name=user.last_name,username=user.username,email=user.email,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user

#endpoint for login
@router.post("/login",response_model=Tokens)
async def login(user:LogIn,db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not await verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=400,detail="not found")
    access_tokens = await create_access_token({"sub":db_user.email})
    return ({"access_tokens":access_tokens,"token_type":"bearer"}) 

















