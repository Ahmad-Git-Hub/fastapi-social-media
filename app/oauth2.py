import jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from app import models, database, schemas
from jwt.exceptions import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings


ALGORITHM = settings.algorithm
SECRET = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
        verified_token = schemas.TokenData(user_id=int(user_id))   
    except PyJWTError:
        raise credentials_exception
    return verified_token
    

def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    verified_token = verify_access_token(token, credentials_exception)

    user_id = verified_token.user_id
    user = db.query(models.User).filter_by(user_id=user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id {user_id} was not found!"
            )
    return user