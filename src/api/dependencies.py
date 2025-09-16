from typing import Annotated

import jwt
from fastapi import Depends, Request, HTTPException, Query
from pydantic import BaseModel

from src.context_manager_db.context_manager import DBManager
from src.db_config import async_session
from src.models import UsersOrm
from src.models.tasks import TaskStatus
from src.services.auth import AuthService
from src.services.users import UserService


async def get_db():
    async with DBManager(async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="You didn't provide token")
    return token


async def get_current_user(db: DBDep, token=Depends(get_token)):
    try:
        data = AuthService.decode_token(token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token signature has expired exception")
    user = await UserService(db).get_user_for_dependencies(user_id_get=data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User did not exist exception")
    return user


async def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService.decode_token(token)
    return data["user_id"]


CurrentUserDep = Annotated[UsersOrm, Depends(get_current_user)]
CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_status(status: TaskStatus = Query(default=TaskStatus.TODO)) -> str:
    return status


StatusDep = Annotated[str, Depends(get_status)]


class PaginationParams(BaseModel):

    page: Annotated[int | None, Query(default=1, description="Номер страницы", ge=1)]
    per_page: Annotated[
        int | None, Query(default=3, description="Кол-во объектов на странице", ge=1, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]
