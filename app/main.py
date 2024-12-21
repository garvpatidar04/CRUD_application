"""Usefull modules"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from contextlib import asynccontextmanager



"""
after alembic we do not need this,  
because alembic will handle all migration and creation task of table in databse
if we keep the below code then it will create the table and the first alemibc version will be useless"""
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    """
    Later"""

    return {'hello, try something'}

# 11:14
# uvicorn app(filename):app(fastapi_appname) --reload