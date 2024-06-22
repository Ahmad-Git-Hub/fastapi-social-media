from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Schema of what should client send to creatposts endpoint
class Post(BaseModel):
    id: Optional[int]
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"id": 592, "title": "Why people leave thier countries!", 
            "content": "let's find out what happened during the 90's",
            "published": True, "rating": 4}]

def find_post(id: int):
    for post in my_posts:
        if(id == post["id"]):
            return post
    return None


@app.get("/")
def root():
    return {"message": "FastApi is here!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post:
        return {"post": post}
    else:
        return "Post was not found!"
    

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"new post created": post_dict}