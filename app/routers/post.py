from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, oauth2, schemas
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostResponseSchema])
def get_posts(db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponseSchema)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter_by(post_id=post_id).first()
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {post_id} was not found!"
            )
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostInputSchema)
def create_post(post: schemas.PostInputSchema, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump())
    new_post.user_id = current_user.user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}")
def delete_post(post_id: int,  db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter_by(post_id=post_id).first()
    if post_to_delete:
        db.delete(post_to_delete)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail= f"post with id {post_id} does not exist!")     
    

@router.put("/{post_id}", response_model=schemas.PostInputSchema)
def update_post(post_id: int, updated_post: schemas.PostInputSchema, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter_by(post_id=post_id)
    retrieved_post = post_query.first()
    if retrieved_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {post_id} does not exist!")
    
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(retrieved_post)
    return retrieved_post
    
