from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db


router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db)):
     # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    # latest_post = cursor.fetchone()
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()  
    if latest_post:
        return latest_post
    else:
         raise HTTPException(
             status_code = status.HTTP_404_NOT_FOUND,
             detail = f"No post was found!"
             )



@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter_by(id=id).first()
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} was not found!"
            )
    

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/posts/{id}")
def delete_post(id: int,  db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM post WHERE id > %s", (id,))
    # rowcount = cursor.rowcount
     # if rowcount > 0:
    #     print(f"rows affected: ", rowcount)
    #     conn.commit()
    post_to_delete = db.query(models.Post).filter_by(id=id).first()
    if post_to_delete:
        db.delete(post_to_delete)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail= f"post with id {id} does not exist!")     
    

# , response_model=schemas.PostResponse
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts
    #                SET title = %s, content = %s, published = %s
    #                WHERE id = %s
    #                RETURNING * """, (post.title, post.content, post.published, id)
    #                )
    # updated_post = cursor.fetchone()
      
    # post_data = updated_post.model_dump(exclude_unset=True) 
    # post_query.update(post_to_update.model)
    # for key, value in post_data.items():
    #     setattr(post_to_update, key, value) 
    post_query = db.query(models.Post).filter_by(id=id)
    retrieved_post = post_query.first()
    if retrieved_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} does not exist!")
    
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(retrieved_post)
    return retrieved_post
    
