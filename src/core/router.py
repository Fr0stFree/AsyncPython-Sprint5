from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session
from .service import ping_db
from . import schemas

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/ping")
async def ping(session: AsyncSession = Depends(get_session)) -> list[schemas.ServiceStatus]:
    response = []
    db_ping = await ping_db(session)
    db_response = schemas.ServiceStatus.build(ping=db_ping, name='database')
    response.append(db_response)
    #  One day there will be more services...
    return response
