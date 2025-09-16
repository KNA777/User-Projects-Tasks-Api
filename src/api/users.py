from fastapi import APIRouter, UploadFile, Depends, Response, HTTPException

from src.exceptions import ObjectNotFoundException, UserNotFoundHTTPException
from src.schemas.users import UserEdit
from src.services.avatars import AvatarService
from src.services.users import UserService

from src.api.dependencies import DBDep, CurrentUserDep, get_current_user, CurrentUserIdDep

router = APIRouter(prefix="/users", tags=["Registration/Authentication/Users"])


@router.get("/get_me")
async def get_me(db: DBDep, current_user: CurrentUserDep):
    user = await UserService(db).get_user(id=current_user.id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("")
async def get_all_users(db: DBDep, current_user: CurrentUserDep):
    try:
        return await UserService(db).get_all_users(current_user=current_user)
    except Exception:
        raise HTTPException(status_code=403, detail="You don't have access rights")


@router.get("/{user_id}")
async def get_user_by_id(
        db: DBDep,
        current_user: CurrentUserDep,
        user_id: int):
    try:
        return await UserService(db).get_user_by_id_with_projects(
            current_user=current_user, user_id_get=user_id)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException


@router.patch("/update_user/{user_id}", dependencies=[Depends(get_current_user)])
async def update_user(
        db: DBDep,
        current_user: CurrentUserDep,
        data: UserEdit,
        user_id: int):
    result = await (UserService(db).
    edit_me(
        data=data,
        current_user=current_user,
        user_id=user_id))
    return result


@router.post("/avatar")
async def user_loading_avatar(
        user_id: CurrentUserIdDep,
        db: DBDep,
        file: UploadFile):
    result = await AvatarService(db).load_avatar(user_id=user_id, file=file)
    return result


@router.delete("/delete/{user_id}", dependencies=[Depends(get_current_user)], summary="User removal")
async def delete_me(
        db: DBDep,
        current_user: CurrentUserDep,
        user_id: int):
    result = await UserService(db).delete_me(current_user=current_user, user_id=user_id)
    return {"status": "ok",
            "deleted_id": result}
