from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import database, schemas, models, utilities

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter_by(email=user_credentials.email).first()
    if not user:
        print("didn't find the user")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utilities.verify_passwords(user_credentials.password, user.password):
        print("compare password")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    return {"token": "not implemented yet"}