from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Schema of what should client send to creatposts endpoint
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"id": 1, "title": "Why people leave thier countries!", 
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

@app.get("/posts/latest")
def get_latest():
    if len(my_posts) > 0:
        post = my_posts[len(my_posts)-1]
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"No post was found!")

    return {'latest post:': post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} was not found!")
    return {"post_details:" : post}
    

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {"new post created": post_dict}

@app.delete("/posts/{id}")
def delete_post(id: int):

    post_to_delete = next((post for post in my_posts if post['id'] == id), None)

    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail= f"post with id {id} does not exist!")

    my_posts.remove(post_to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_to_update = next((post for post in my_posts if post['id'] == id), None)
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail= f"post with id {id} does not exist!")
    else:
        post_to_update.update(post.model_dump(exclude_unset=True))
        return {"updated post": post_to_update}  
