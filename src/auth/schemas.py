from pydantic import BaseModel, UUID4, HttpUrl, validator, Field

from .settings import settings


class UserBase(BaseModel):
    username: str = Field(..., min_length=settings.MIN_USERNAME_LENGTH,
                               max_length=settings.MAX_USERNAME_LENGTH)


class UserCreate(UserBase):
    password: str = Field(..., min_length=settings.MIN_PASSWORD_LENGTH,
                               max_length=settings.MAX_PASSWORD_LENGTH)
    

class UserUpdate(UserCreate):
    pass
    
    
class UserDB(UserBase):
    id: UUID4
    hashed_password: str
