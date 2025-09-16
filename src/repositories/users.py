from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions import ObjectNotFoundException
from src.models import UsersOrm, ProjectsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.users import UserMapper
from src.schemas.users import UserWithHashedPassword, UserWithRels


class UserRepository(BaseRepository):

    model = UsersOrm
    mapper = UserMapper


    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        try:
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPassword.model_validate(model, from_attributes=True)


    async def load_new_user_avatar_to_db(self, user_id, avatar_url):
        stmt = update(self.model).filter_by(id=user_id).values(avatar_url=avatar_url)
        await self.session.execute(stmt)
        await self.session.commit()

        # return result.mappings().first()

    async def get_user_with_projects(self, user_id):
        query = (select(self.model)
                 .options(joinedload(self.model.projects))
                 .filter_by(id=user_id))
        result = await self.session.execute(query)
        users = result.unique().scalars().all()
        if not users:
            raise ObjectNotFoundException
        return [
            UserWithRels.model_validate(model, from_attributes=True)
            for model in users
        ]

    async def get_all_users_projects_ids(self, user_id):
        query = select(self.model.id).where(ProjectsOrm.owner_id == user_id)
        data = await self.session.execute(query)
        projects_ids = data.scalars().all()
        return projects_ids