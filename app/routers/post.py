from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, oauth2, schemas
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponseSchema])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponseSchema)
def get_post(
    post_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter_by(post_id=post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found!"
            )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostInputSchema)
def create_post(
    post: schemas.PostInputSchema,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_post = models.Post(user_id=current_user.user_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,  db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    post_to_delete = db.query(models.Post).filter_by(post_id=post_id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"post with id {post_id} does not exist!")     
    
    if post_to_delete.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detial="Not authorized to perform delete")
    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)          


@router.put("/{post_id}", response_model=schemas.PostInputSchema)
def update_post(
    post_id: int, updated_post: schemas.PostInputSchema,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter_by(post_id=post_id)
    post_to_update = post_query.first()
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} does not exist!")
    
    if post_to_update.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detial="Not authorized to perform update")
    
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update
    
