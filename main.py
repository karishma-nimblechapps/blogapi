from fastapi import FastAPI
from app.routers import blog_router,user_router,auth_router


app=FastAPI()

@app.get("/")
def check_server():
    return{"Message":"Server is running"}

app.include_router(user_router.router,prefix="/users",tags=["users"])
app.include_router(blog_router.router,prefix="/blogs",tags=["blogs"])
app.include_router(auth_router.router,prefix="/auths",tags=["auths"])

