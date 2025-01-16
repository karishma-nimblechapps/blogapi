from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db,User
from app.schemas import UserCreate, UserInResponse, UserUpdate,ToggleUpdate
from typing import List

router=APIRouter()

#get all the users
@router.get("/",response_model=List[UserInResponse])
async def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users

#get users by id
@router.get("/{user_id}",response_model=UserInResponse)
async def read_users(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return user

#update users by id
@router.put("/{user_id}",response_model=UserInResponse)
async def update_users(user_id:int,user:UserUpdate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    for key,value in user.model_dump().items():
        setattr(existing_user,key,value)
    db.commit()
    db.refresh(existing_user)
    return existing_user

#delete users by id
@router.delete("/{user_id}")
async def delete_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()

#defining a function for updating status
def update_status_user(db:Session,user_id:int,status:bool):
    user_status=db.query(User).filter(User.id == user_id).first()
    if user_status:
        user_status.status = status
        db.commit()
        db.refresh(user_status)
    return user_status

#update status by id
@router.patch("/changestatus/{user_id}",response_model=UserInResponse)
def toggle_update_status(user_id:int,status_update:ToggleUpdate,db:Session=Depends(get_db)):
    toggle_user = update_status_user(db,user_id,status_update.status)
    if not toggle_user:
        raise HTTPException(status_code=404,detail="not found")
    return toggle_user 

    







