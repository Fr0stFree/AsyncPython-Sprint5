from http import HTTPStatus
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import RedirectResponse, Response
from pydantic import HttpUrl, AnyUrl
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session
from . import schemas
from .service import User


router = APIRouter()