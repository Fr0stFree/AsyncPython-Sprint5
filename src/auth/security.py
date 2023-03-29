import time
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from base.settings import settings as global_settings
from .settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(username: str) -> str:
    payload = {"username": username, "expires": time.time() + settings.TOKEN_EXPIRES_AFTER}
    token = jwt.encode(payload, key=global_settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
    return token


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, key=global_settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Token is invalid")

    expire = payload.get("expires")

    if expire is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Token is invalid")
    if time.time() > expire:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Token is expired")
    return payload
