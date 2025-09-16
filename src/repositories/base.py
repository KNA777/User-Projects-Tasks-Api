from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from src.repositories.mapper.base import DataMapper
from asyncpg.exceptions import UniqueViolationError


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        data = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in data.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        data = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(data.scalars().one())


    async def get_one_or_none(self, data: BaseModel):
        query = select(self.model).filter_by(**data.model_dump())
        data = await self.session.execute(query)
        result = data.scalars().one_or_none()
        if result is None:
            return None
        return self.mapper.map_to_domain_entity(result)

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExistsException
        await self.session.commit()
        return self.mapper.map_to_domain_entity(result.scalars().one())


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = (update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()

        return self.mapper.map_to_domain_entity(result.scalars().one())


    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        try:
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except NoResultFound:
            raise ObjectNotFoundException



