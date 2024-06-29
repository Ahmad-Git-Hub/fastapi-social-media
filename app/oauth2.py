import jwt
from datetime import datetime, timedelta
from . import variables

ALGORITHM = 'HS256'
SECRET = variables.SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)
    return encoded_jwt
