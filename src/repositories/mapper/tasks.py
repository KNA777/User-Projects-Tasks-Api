from sqlalchemy import select

from src.models import TasksOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.tasks import TasksResponse, TasksResponseWithComments


class TaskMapper(DataMapper):
    db_model = TasksOrm
    schema = TasksResponse

