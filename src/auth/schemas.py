from pydantic import BaseModel, Field

from .settings import settings


class UserBase(BaseModel):
    username: str = Field(..., min_length=settings.MIN_USERNAME_LENGTH,
                          max_length=settings.MAX_USERNAME_LENGTH)


class UserCreate(UserBase):
    password: str = Field(..., min_length=settings.MIN_PASSWORD_LENGTH,
                          max_length=settings.MAX_PASSWORD_LENGTH)


class UserLogin(UserCreate):
    pass


class UserUpdate(UserCreate):
    pass


class UserCreatedResponse(UserBase):
    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


