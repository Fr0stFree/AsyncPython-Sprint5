from uuid import UUID

from pydantic import HttpUrl, AnyUrl
from sqlalchemy.ext.asyncio import AsyncSession

from base.service import RepositoryInterface
from .models import User as UserModel
from .schemas import UserCreate, UserUpdate


class UserRepository(RepositoryInterface[UserModel, UserCreate, UserUpdate]):
    pass
    

User = UserRepository(UserModel)