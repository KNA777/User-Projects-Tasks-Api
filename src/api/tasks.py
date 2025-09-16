from fastapi import APIRouter, Depends

from src.api.dependencies import DBDep, get_current_user, StatusDep, PaginationDep
from src.schemas.tasks import TasksRequest, TasksEditRequest
from src.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.post("/add/project/{project_id}", dependencies=[Depends(get_current_user)])
async def create_task(status: StatusDep, data: TasksRequest, db: DBDep, project_id: int):
    task = await TasksService(db).create_task(data=data, project_id=project_id, status=status)
    return task


@router.patch("/edit/{task_id}")
async def update_task(db: DBDep, task_id: int, status: StatusDep, data: TasksEditRequest):
    updated_task = await TasksService(db).edit_task(data=data, task_id=task_id, status=status)
    return updated_task


@router.delete("/delete/{task_id}")
async def delete_task(db: DBDep, task_id: int):
    deleted_task = await TasksService(db).delete_task(task_id=task_id)
    return deleted_task

@router.get("/get/projects/{project_id}")
async def get_all_tasks_of_project_by_id(db: DBDep, project_id: int, pagination: PaginationDep):
    tasks_of_project = await TasksService(db).get_all_tasks_of_project(
        project_id=project_id,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )
    return tasks_of_project
