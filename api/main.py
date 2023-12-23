from fastapi import FastAPI
import uvicorn
from .routes import users, auth, blog_content
from . import oath2


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(oath2.router)
app.include_router(blog_content.router)