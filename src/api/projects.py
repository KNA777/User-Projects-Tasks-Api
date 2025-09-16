from fastapi import APIRouter, Depends

from src.schemas.projects import ProjectRequest

from src.api.dependencies import DBDep, CurrentUserDep, get_current_user, PaginationDep
from src.services.projects import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"], dependencies=[Depends(get_current_user)])


@router.post("")
async def add_project(current_user: CurrentUserDep, db: DBDep, data: ProjectRequest):
    result = await ProjectService(db).create_project(data=data, user_id=current_user.id)
    return result


@router.patch("/edit/{project_id}")
async def update_project(current_user: CurrentUserDep, db: DBDep, data: ProjectRequest, project_id: int):
    result = await ProjectService(db).edit_project(data=data, user_id=current_user.id, project_id=project_id)
    return result


@router.delete("/delete/{project_id}")
async def delete_project(current_user: CurrentUserDep, db: DBDep, project_id: int):
    deleted_project = await ProjectService(db).delete_project(user_id=current_user.id, project_id=project_id)
    return {
        "deleted project": deleted_project
    }

@router.get("")
async def get_all_user_projects(current_user: CurrentUserDep, db: DBDep, pagination: PaginationDep):
    user_projects = await ProjectService(db).get_all_user_projects(
        user_id=current_user.id,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1))
    return {
        "user id:": current_user.id,
        "projects": user_projects
    }

@router.get("/{project_id}")
async def get_one_user_project_with_details(current_user: CurrentUserDep, db: DBDep, project_id: int):
    project = await ProjectService(db).get_user_project_details_by_id(
        user_id=current_user.id, project_id=project_id)
    return project
