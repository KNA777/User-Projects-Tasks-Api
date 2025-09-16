from datetime import datetime

from pydantic import BaseModel


class CommentsRequest(BaseModel):

    content: str


class CommentsAdd(CommentsRequest):

    task_id: int
    author_id: int


class Comments(BaseModel):
    id: int
    content: str
    task_id: int
    author_id: int
    created_at: datetime


class CommentsResponseWithTasks(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime


class CommentsWithOutTaskId(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime
