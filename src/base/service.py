from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base


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
    def __init__(self, model: type[ModelType]):
        self._model = model

    async def get(self, session: AsyncSession, **options) -> ModelType:
        statement = select(self._model).filter_by(**options)
        result = await session.execute(statement)
        return result.scalar_one()

    async def filter(self, session: AsyncSession, *, offset: int = 0,
                     limit: int = 100, **options) -> Sequence[ModelType]:
        statement = select(self._model).filter_by(**options) \
                                       .offset(offset) \
                                       .limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()

    async def create(self, session: AsyncSession, schema: CreateSchemaType) -> ModelType:
        statement = insert(self._model).values(schema.dict()) \
                                       .returning(self._model)
        result = await session.execute(statement)
        await session.commit()
        return result.scalar_one()

    async def bulk_create(self, session: AsyncSession,
                          schema: Sequence[CreateSchemaType]) -> Sequence[ModelType]:
        statement = insert(self._model).values([row.dict() for row in schema]) \
                                       .returning(self._model)
        result = await session.execute(statement)
        await session.commit()
        return result.scalars().all()

    async def update(self, session: AsyncSession,
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

