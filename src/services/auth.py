from datetime import datetime, timezone, timedelta

from fastapi import Response, HTTPException
import jwt
from passlib.context import CryptContext

from src.exceptions import UserPasswordException, SuperUserPasswordException
from src.schemas.users import UserRegRequest, UserLogin
from src.services.base import BaseService
from src.settings_config import settings


class AuthService(BaseService):
    pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_contex.verify(plain_password, hashed_password)

    @classmethod
    def create_hashed_password(cls, password):
        return cls.pwd_contex.hash(password)

    async def registration(self, data: UserRegRequest):
        hashed_password = self.create_hashed_password(password=data.password)
        if data.superuser_psw and data.superuser_psw != settings.SUPERUSER_PASSWORD:
            raise SuperUserPasswordException
        data_to_db = data.user_add(hashed_password)
        return await self.db.user.add(data_to_db)

    async def login(self, data: UserLogin, response: Response):
        user = await self.db.user.get_user_hashed_password(email=data.email)
        if not self.verify_password(plain_password=data.password, hashed_password=user.hashed_password):
            raise UserPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token
