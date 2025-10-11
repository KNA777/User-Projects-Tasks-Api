from fastapi import Body
from pydantic import BaseModel, EmailStr

from src.schemas.projects import Projects
from src.settings_config import settings


class UserRegRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Body(..., min_length=6, max_length=18)
    superuser_psw: str | None = None

    @staticmethod
    def validate_superuser_psw(token):
        if not token:
            return False

        from secrets import compare_digest

        return compare_digest(token, settings.SUPERUSER_PASSWORD)

    def user_add(self, hashed_password: str):
        is_superuser = self.validate_superuser_psw(self.superuser_psw)
        return UserAdd(
            **self.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
            is_superuser=is_superuser,
        )


class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_superuser: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool


class UserWithRels(User):
    projects: list[Projects]


class UserWithHashedPassword(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str


class UserEdit(BaseModel):
    username: str | None = None
    avatar_url: str | None = None
    is_superuser: bool | None = False
