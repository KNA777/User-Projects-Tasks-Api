from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload

from src.models import TasksOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.tasks import TaskMapper
from src.schemas.tasks import TasksResponseWithComments


class TaskRepository(BaseRepository):

    model = TasksOrm
    mapper = TaskMapper

    async def get_all_tasks_with_comments(
            self,
            project_id,
            limit,
            offset):
        query = (select(self.model)
                 .options(joinedload(self.model.comments))
                 .filter_by(project_id=project_id)
                 .limit(limit)
                 .offset(offset))
        data = await self.session.execute(query)
        return [
            TasksResponseWithComments.model_validate(
                model, from_attributes=True) for model in data.unique().scalars().all()]



