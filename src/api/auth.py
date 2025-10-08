from fastapi import APIRouter, Response, Body

from src.api.dependencies import DBDep
from src.constants import OPENAPI_EXAMPLES_REG, OPENAPI_EXAMPLES_LOGIN
from src.exceptions import (ObjectAlreadyExistsException, MailAlreadyExistHTTPException,
                            UserPasswordException,ObjectNotFoundException,
                            PasswordHTTPException, MailHTTPException,
                            SuperUserPasswordException, SuperUserPasswordHTTPException)
from src.schemas.users import UserRegRequest, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Registration/Authentication/Users"])


@router.post("/registration")
async def user_registration(
        db: DBDep,
        data: UserRegRequest = Body(openapi_examples=OPENAPI_EXAMPLES_REG)
):
    try:
        user = await AuthService(db).registration(data=data)
    except ObjectAlreadyExistsException:
        raise MailAlreadyExistHTTPException
    except SuperUserPasswordException:
        raise SuperUserPasswordHTTPException
    return user


@router.post("/login")
async def user_login(
        db: DBDep,
        response: Response,
        data: UserLogin = Body(openapi_examples=OPENAPI_EXAMPLES_LOGIN),
):
    try:
        access_token = await AuthService(db).login(data=data, response=response)
    except (UserPasswordException, ObjectNotFoundException) as ex:
        if isinstance(ex, UserPasswordException):
            raise PasswordHTTPException
        raise MailHTTPException
    return {"access_token": access_token}
