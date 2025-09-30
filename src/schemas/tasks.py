from pydantic import BaseModel

from src.models.tasks import TaskStatus
from src.schemas.comments import CommentsResponseWithTasks


class TasksResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    project_id: int
    assignee_id: int


class TasksResponseWithComments(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    project_id: int
    assignee_id: int
    comments: list[CommentsResponseWithTasks]


class TasksRequest(BaseModel):
    title: str
    description: str
    assignee_id: int


class TasksAdd(TasksRequest):
    project_id: int
    status: str


class TasksEditRequest(TasksRequest):
    pass


class TasksEditAdd(TasksEditRequest):
    status: str
