from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostInputSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    user_id: int
    post_id: int
    created_at: datetime
    post_owner: UserResponseSchema

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None



