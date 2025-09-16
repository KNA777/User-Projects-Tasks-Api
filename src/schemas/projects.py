from pydantic import BaseModel, Field

from src.schemas.tasks import TasksResponse


class ProjectRequest(BaseModel):
    name: str
    description: str


class ProjectAdd(BaseModel):
    name: str
    description: str
    owner_id: int


class Projects(ProjectAdd):
    id: int


class ProjectsEdit(ProjectRequest):
    pass


class ProjectsResponse(ProjectRequest):
    id: int


class ProjectWithTasksResponse(BaseModel):
    id: int
    name: str
    description: str
    tasks: list[TasksResponse]
