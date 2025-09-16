from fastapi import APIRouter, Depends

from src.exceptions import ObjectAlreadyExistsException, TaskExistsHTTPException
from src.schemas.comments import CommentsRequest

from src.api.dependencies import DBDep, CurrentUserIdDep, PaginationDep
from src.services.comments import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/add/tasks/{task_id}")
async def add_comment_to_task(
        current_user_id: CurrentUserIdDep,
        db: DBDep,
        data: CommentsRequest,
        task_id: int):
    try:
        created_comment = await CommentService(db).create_comment_to_task(
            data=data, task_id=task_id, author_id=current_user_id)
    except ObjectAlreadyExistsException:
        raise TaskExistsHTTPException
    return created_comment


@router.get("/get/tasks/{task_id}")
async def get_all_task_comments_by_id(db: DBDep, pagination: PaginationDep, task_id: int):
    comments = await CommentService(db).get_task_comments_by_id(
        task_id=task_id,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )
    return comments
