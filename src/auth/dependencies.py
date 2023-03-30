from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session

from . import schemas
from .security import oauth2_scheme, verify_access_token, verify_password
from .service import User


async def unique_user(schema: schemas.UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    try:
        user = await User.create(session, schema=schema)
        return user
    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f"Username '{schema.username}' already taken")


async def verified_user(schema: schemas.UserLogin, session: AsyncSession = Depends(get_session)) -> User:
    try:
        user = await User.get(session, username=schema.username)
    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(schema.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")
    return user


async def authentication(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Sign in required")
    decoded_token = verify_access_token(token)
    return decoded_token["username"]
