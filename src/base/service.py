from typing import Generic, Type, TypeVar, Sequence

import sqlalchemy.exc
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base
from .exceptions import ObjectAlreadyExists, ObjectDoesNotExist, MultipleObjectsReturned


class Repository:
    
    def get(self, *args, **kwargs):
        raise NotImplementedError
    
    def filter(self, *args, **kwargs):
        raise NotImplementedError
    
    def create(self, *args, **kwargs):
        raise NotImplementedError
    
    def update(self, *args, **kwargs):
        raise NotImplementedError
    
    def delete(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryInterface(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model
    
    async def get(self, session: AsyncSession, **options) -> ModelType:
        statement = select(self._model).filter_by(**options)
        result = await session.execute(statement)
        try:
            return result.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectDoesNotExist
        except sqlalchemy.exc.MultipleResultsFound:
            raise MultipleObjectsReturned

    async def filter(self, session: AsyncSession, *, offset: int = 0,
                     limit: int = 100, **options) -> Sequence[ModelType]:
        statement = select(self._model).filter_by(**options) \
                                       .offset(offset) \
                                       .limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, *, schema: CreateSchemaType) -> ModelType:
        statement = insert(self._model).values(schema.dict()) \
                                       .returning(self._model)
        try:
            result = await session.execute(statement)
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
            raise ObjectAlreadyExists
        await session.commit()
        return result.scalar_one()
    
    async def bulk_create(self, session: AsyncSession, *,
                          schema: Sequence[CreateSchemaType]) -> Sequence[ModelType]:
        statement = insert(self._model).values([row.dict() for row in schema]) \
                                       .returning(self._model)
        try:
            result = await session.execute(statement)
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
            raise ObjectAlreadyExists
        await session.commit()
        return result.scalars().all()
    
    async def update(self, session: AsyncSession, *,
                     schema: UpdateSchemaType, **options) -> ModelType:
        obj = await self.get(session, **options)
        statement = update(self._model).where(obj.id == self._model.id) \
                                       .values(schema.dict()) \
                                       .returning(self._model)
        result = await session.execute(statement)
        await session.commit()
        return result.scalar_one()

    async def delete(self, session: AsyncSession, **options) -> ModelType:
        obj = await self.get(session, **options)
        statement = delete(self._model).where(self._model.id == obj.id) \
                                       .returning(self._model)
        result = await session.execute(statement)
        await session.commit()
        return result.scalar_one()
