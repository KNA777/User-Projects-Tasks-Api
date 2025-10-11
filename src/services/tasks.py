from src.api.dependencies import StatusDep
from src.exceptions import ObjectNotFoundException, TaskExistsHTTPException
from src.schemas.tasks import TasksRequest, TasksAdd, TasksEditRequest, TasksEditAdd
from src.services.base import BaseService
from src.services.notifications import NotificationService


class TasksService(BaseService):

    async def create_task(self, data: TasksRequest, project_id: int, status: StatusDep):
        new_data = TasksAdd(**data.model_dump(), project_id=project_id, status=status)
        task = await self.db.task.add(new_data)
        if task.assignee_id:
            project = await self.db.project.get_one(id=project_id)

            await NotificationService.send_task_assigned_notification(
                user_id=task.assignee_id,
                task_id=task.id,
                task_title=task.title,
                project_name=project.name
            )
        return task

    async def edit_task(self, data: TasksEditRequest, task_id, status):
        new_data = TasksEditAdd(**data.model_dump(), status=status)
        task = await self.db.task.edit(new_data, id=task_id)
        if hasattr(data, 'assignee_id') and data.assignee_id is not None:
            project = await self.db.project.get_one(id=task.project_id)

            await NotificationService.send_task_assigned_notification(
                user_id=data.assignee_id,
                task_id=task_id,
                task_title=task.title,
                project_name=project.name
            )
        return task

    async def delete_task(self, task_id):
        try:
            deleted_task = await self.db.task.delete(id=task_id)
        except ObjectNotFoundException:
            raise TaskExistsHTTPException
        return deleted_task

    async def get_all_tasks_of_project(self, project_id, limit, offset):
        tasks_of_project = await self.db.task.get_all_tasks_with_comments(
            project_id=project_id,
            limit=limit,
            offset=offset)
        return tasks_of_project
