from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone
from . import variables, schemas
from jwt.exceptions import PyJWTError
from fastapi.security import OAuth2PasswordBearer


ALGORITHM = variables.ALGORITHM
SECRET = variables.SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, variables.SECRET, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id='id')
    except PyJWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token : str = Depends(oauth2_scheme)):    
    return verify_access_token(token)