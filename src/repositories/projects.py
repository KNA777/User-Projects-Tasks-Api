from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models import ProjectsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.projects import ProjectMapper
from src.schemas.projects import ProjectsResponse, ProjectWithTasksResponse


class ProjectRepository(BaseRepository):

    model = ProjectsOrm
    mapper = ProjectMapper


    async def get_user_projects_ids(self, user_id):
        query = select(self.model.id).filter_by(owner_id=user_id)
        ids_project_by_user = await self.session.execute(query)
        return ids_project_by_user.scalars().all()


    async def get_all_user_projects(self, user_id, limit, offset):
        query = (select(self.model)
                 .filter_by(owner_id=user_id)
                 .limit(limit)
                 .offset(offset))
        all_user_project = await self.session.execute(query)
        return [
            ProjectsResponse.model_validate(
                model, from_attributes=True) for model in all_user_project.scalars().all()]


    async def get_user_project_with_tasks(self, **filter_by):
        query = ((select(self.model)
                 .options(joinedload(self.model.tasks)))
                 .filter_by(**filter_by))

        project = await self.session.execute(query)
        data = project.unique().scalars().one()
        return ProjectWithTasksResponse.model_validate(
                data, from_attributes=True)
