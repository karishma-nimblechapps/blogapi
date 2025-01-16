from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db, Blog
from app.schemas import BlogCreate, BlogInDB, BlogUpdate, BlogResponse, ToggleUpdate
from typing import List

router=APIRouter()

#creating a blog
@router.post("/",response_model=BlogInDB)
async def create_blog(blog:BlogCreate,db:Session=Depends(get_db)):
    db_blog=Blog(**blog.model_dump())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

#returning all blogs
@router.get("/",response_model=List[BlogInDB])
async def get_blogs(db:Session=Depends(get_db)):
    blogs=db.query(Blog).all()
    return blogs

#get_blog_by_id
@router.get("/{blog_id}",response_model=BlogInDB)
async def read_blogs(blog_id:int,db:Session=Depends(get_db)):
    blog=db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail=" blog not found")
    return blog

#update the blog 
@router.put("/{blog_id}",response_model=BlogInDB)
async def update_blog(blog_id:int,blog:BlogUpdate,db:Session=Depends(get_db)):
    existing_blogs=db.query(Blog).filter(Blog.id == blog_id).first()
    if existing_blogs is None:
        raise HTTPException(status_code=404,detail="blogs not found")
    for key, value in blog.model_dump().items():
        setattr(existing_blogs, key, value)
    db.commit()
    db.refresh(existing_blogs)
    return existing_blogs

#delete the blog
@router.delete("/{blog_id}",response_model=BlogInDB)
async def delete_blog(blog_id:int,db:Session=Depends(get_db)):
    blog=db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail="blog not found")
    db.delete(blog)
    db.commit()

#definig a function for update of the status(true/false) of blog
def update_status_blog(db:Session,blog_id:int,status:bool):
    blog_status=db.query(Blog).filter(Blog.id == blog_id).first()
    if blog_status:
        blog_status.status = status
        db.commit()
        db.refresh(blog_status)
    return blog_status

#changing the status (active/inactive=true/false)
@router.patch("/changestatus/{blog_id}",response_model=BlogResponse)
def toggle_updateblog_status(user_id:int,status_update:ToggleUpdate,db:Session=Depends(get_db)):
    toggle_blog = update_status_blog(db,user_id,status_update.status)
    if not toggle_blog:
        raise HTTPException(status_code=404,detail="not found")
    return toggle_blog


#individual adding and removing of blogs from the top
##adding blogs to the top
def update_blog_top_with_add(db:Session, add_top_blog_ids: List[int]):

    if len(add_top_blog_ids) > 3:
        raise HTTPException(status_code=400, detail="Cannot select more than 3 blogs as top blogs.")
    if add_top_blog_ids:
        blogs_to_add = db.query(Blog).filter(Blog.id.in_(add_top_blog_ids)).all()
        if len(blogs_to_add) + db.query(Blog).filter(Blog.is_top == True).count() > 3:
            raise HTTPException(status_code=400, detail="Cannot have more than 3 top blogs at a time.")
        
        for blog in blogs_to_add:
            blog.is_top = True

    db.commit()
    return db.query(Blog).filter(Blog.is_top == True).all()

@router.post("/top-add",response_model=List[BlogResponse])
def update_top_blogs_add( 
    add_top_blog_ids: List[int] = [], 
    db: Session = Depends(get_db)):

    update_top_blogs_add = update_blog_top_with_add(db,add_top_blog_ids)
    return update_top_blogs_add

#removinng blogs from the top
def update_blog_top_with_removal(db: Session,remove_top_blog_ids: List[int]):
   
    # Remove the specified blogs from the top
    if remove_top_blog_ids:
        blogs_to_remove = db.query(Blog).filter(Blog.id.in_(remove_top_blog_ids)).all()
        if not blogs_to_remove:
            raise HTTPException(status_code=404, detail="No blogs found with the given IDs to remove.")
        
        for blog in blogs_to_remove:
            blog.is_top = False

        db.commit()
        return db.query(Blog).filter(Blog.is_top == False).all()

@router.post("/top-remove", response_model=List[BlogResponse])
def update_top_blogs_remove(
    remove_top_blog_ids: List[int] = [], 
    db: Session = Depends(get_db)):
   
    updated_top_blogs_remove = update_blog_top_with_removal(db,remove_top_blog_ids)
    return updated_top_blogs_remove

#updating adding & removing blogs from the top together 
def update_with_add_removal(db:Session,update_top_add:List[int],update_top_remove:List[int]):
    if len (update_top_add) >3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="cannot more than 3")
    
    if update_top_add:
        blog_to_add = db.query(Blog).filter(Blog.id.in_(update_top_add)).all()
        if len(blog_to_add) + db.query(Blog).filter(Blog.is_top == True).count() > 3:
            raise HTTPException(status_code=400, detail="Cannot have more than 3 top blogs at a time.")

        blog_to_add = db.query(Blog).filter(Blog.id.in_(update_top_add)).all()
        if len(blog_to_add) + db.query(Blog).filter(Blog.is_top == True).count() > 3:
            raise HTTPException(status_code=400, detail="Cannot accept more than 3")
                                
        for blog in blog_to_add:
            blog.is_top = True   
            
    if update_top_remove:
        blog_to_remove = db.query(Blog).filter(Blog.id.in_(update_top_remove)).all()
        if not blog_to_remove:
            raise HTTPException(status_code=404, detail="No blogs found with the given IDs to remove.")
        
        for blog in blog_to_remove:
            blog.is_top = False

    
                             
    db.commit()
    return db.query(Blog).filter(Blog.is_top == True).all()
    
@router.post("/top-remove-add",response_model=List[BlogResponse])
def top_remove_add(update_top_add:List[int]=[],
                   update_top_remove:List[int]=[],
                   db:Session=Depends(get_db)):
    updated_edition = update_with_add_removal(db,update_top_add,update_top_remove)
    return updated_edition

    