from datetime import datetime
from pydantic import BaseModel, EmailStr

# Schema of what should client send to path operation
class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostInputSchema(PostBaseSchema):
    pass


# Schema of what response should look like
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



