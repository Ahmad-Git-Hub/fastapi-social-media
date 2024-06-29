from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostInputSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    



