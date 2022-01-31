from pydantic import BaseModel

class PostResponse(BaseModel):
    id: int
    title: str
    content: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str