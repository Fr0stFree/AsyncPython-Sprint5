from sqlalchemy.ext.asyncio import AsyncSession

from base.service import RepositoryInterface

from .models import User as UserModel
from .schemas import UserCreate, UserUpdate
from .security import create_hashed_password


class UserRepository(RepositoryInterface[UserModel, UserCreate, UserUpdate]):
    async def create(self, session: AsyncSession, schema: UserCreate) -> UserModel:
        schema.password = create_hashed_password(schema.password)
        return await super().create(session, schema)
    

User = UserRepository(UserModel)
