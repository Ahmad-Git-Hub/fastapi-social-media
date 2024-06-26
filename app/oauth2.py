import jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from app import models, database, schemas, variables
from jwt.exceptions import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


ALGORITHM = variables.ALGORITHM
SECRET = variables.SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, variables.SECRET, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))   
    except PyJWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    verified_token = verify_access_token(token, credentials_exception)

    id = int(verified_token.id)
    user = db.query(models.User).filter_by(id=id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} was not found!"
            )
    return user