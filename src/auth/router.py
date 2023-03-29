from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session
from . import schemas
from .dependencies import verified_user, unique_user, authentication
from .security import create_access_token
from .service import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/sign-up', response_model=schemas.UserCreatedResponse, status_code=HTTPStatus.CREATED)
async def sign_up(user: User = Depends(unique_user)):
    return user


@router.post('/sign-in', response_model=schemas.TokenResponse, status_code=HTTPStatus.OK)
async def sign_in(user: User = Depends(verified_user)):
    token = create_access_token(user.username)
    return schemas.TokenResponse(access_token=token, token_type="bearer")


@router.get('/me', response_model=schemas.UserCreatedResponse, status_code=HTTPStatus.OK)
async def get_me(username: str = Depends(authentication), session: AsyncSession = Depends(get_session)):
    user = await User.get(session, username=username)
    return user

