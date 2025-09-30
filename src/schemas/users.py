from fastapi import Body
from pydantic import BaseModel, EmailStr

from src.schemas.projects import Projects


class UserRegRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Body(..., min_length=6, max_length=18)
    superuser_psw: str | None = None

    def user_add(self, hashed_password: str):
        if self.superuser_psw:
            return UserAddSuperUserTrue(
                **self.model_dump(exclude={"password"}),
                hashed_password=hashed_password
            )
        return UserAddSuperUserFalse(
            **self.model_dump(exclude={"password"}),
                hashed_password=hashed_password
            )


class UserAddSuperUserTrue(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_superuser: bool = True


class UserAddSuperUserFalse(UserAddSuperUserTrue):
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
