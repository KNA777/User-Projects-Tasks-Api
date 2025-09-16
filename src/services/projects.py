from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select

from src.schemas.projects import ProjectAdd, ProjectRequest, ProjectsEdit
from src.services.base import BaseService


class ProjectService(BaseService):

    async def create_project(self, data: ProjectRequest, user_id):
        new_data = ProjectAdd(**data.model_dump(), owner_id=user_id)
        return await self.db.project.add(new_data)

    async def edit_project(self, data: ProjectRequest, user_id, project_id):
        user_project_ids = await self.db.project.get_user_projects_ids(user_id)
        if not project_id in user_project_ids:
            raise HTTPException(status_code=403, detail="Permission denied")
        try:
            return await self.db.project.edit(data, owner_id=user_id, id=project_id)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Unique exception")

    async def delete_project(self, user_id, project_id):
        user_project_ids = await self.db.project.get_user_projects_ids(user_id)
        if not project_id in user_project_ids:
            raise HTTPException(status_code=403, detail="Permission denied")
        return await self.db.project.delete(id=project_id)

    async def get_all_user_projects(self, user_id, limit, offset):
        user_projects = await self.db.project.get_all_user_projects(
            user_id, limit, offset)
        return user_projects

    async def get_user_project_details_by_id(self, user_id, project_id):
        user_project_ids = await self.db.project.get_user_projects_ids(user_id)
        if not project_id in user_project_ids:
            raise HTTPException(status_code=404, detail="Permission denied")
        project = await self.db.project.get_user_project_with_tasks(id=project_id)
        return project
