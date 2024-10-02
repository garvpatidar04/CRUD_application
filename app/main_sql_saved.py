"""Usefull modules"""
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

# uvicorn app.main:app --reload

load_dotenv(dotenv_path='app\.env')
db_password =  os.getenv("DB_PASSWORD")

# print(db_password)

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password=db_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to databse is successful")
        break
    except Exception as error:
        print("Connection failed")
        print(F"Error: {error}")
        time.sleep(3)
    

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePost(BaseModel):
    title: str = None
    content: str = None
    published: bool = None

app = FastAPI()

@app.get("/")
def root():
    """
    Later"""

    return {'hello, try something'}


@app.get("/posts")
def get_posts():
    """"
    Just return the post"""
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Creates a entry in our database"""

    cursor.execute(""" INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"Post Created": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post_id = cursor.fetchone()

    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=F"Post with id {id} was not found")
    return {"Post": post_id}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=F"Post with id {id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, new_post: UpdatePost):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(new_post.title, new_post.content, new_post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=F"Post with id {id} was not found")
    return {'post is updated': updated_post}

