from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utilities
from app.database import get_db

router = APIRouter(prefix="/users")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user (user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utilities.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user     


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} was not found!"
            )
    return user
    
