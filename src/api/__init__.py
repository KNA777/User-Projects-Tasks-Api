from fastapi import APIRouter
from src.api.users import router as user_router
from src.api.auth import router as auth_router
from src.api.projects import router as project_router
from src.api.tasks import router as task_router
from src.api.comments import router as comment_router
from src.api.notifications import router as notification_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(project_router)
main_router.include_router(task_router)
main_router.include_router(comment_router)
main_router.include_router(notification_router)
