from datetime import datetime
from pydantic import BaseModel

# Schema of what should client send to path operation
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


# Schema of what response should look like
class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

