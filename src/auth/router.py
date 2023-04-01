from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session

from . import schemas
from .dependencies import authentication, unique_user, verified_user
from .security import create_access_token
from .service import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/sign-up', status_code=HTTPStatus.CREATED)
async def sign_up(user: User = Depends(unique_user)) -> schemas.UserCreatedResponse:
    return user


@router.post('/sign-in')
async def sign_in(user: User = Depends(verified_user)) -> schemas.TokenResponse:
    token = create_access_token(user.id)
    return schemas.TokenResponse(access_token=token, token_type="bearer")


@router.get('/me')
async def get_me(user_id: UUID = Depends(authentication),
                 session: AsyncSession = Depends(get_session)) -> schemas.UserCreatedResponse:
    user = await User.get(session, id=user_id)
    return user

