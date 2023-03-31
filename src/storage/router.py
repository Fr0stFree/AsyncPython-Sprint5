from http import HTTPStatus
from pathlib import PosixPath
from uuid import UUID
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session

from . import schemas
from .service import StoredFile
from .settings import settings
from auth.dependencies import authentication

router = APIRouter(prefix="/storage", tags=["storage"])


@router.post('/upload', status_code=HTTPStatus.CREATED)
async def upload_file(*, file: UploadFile = File(...),
                      path: PosixPath = Form(...),
                      is_private: bool = Form(False),
                      # user_id: UUID = Depends(authentication),
                      session: AsyncSession = Depends(get_session)):
    random_uuid = UUID('00000000-0000-0000-0000-000000000000')
    content = await file.read()
    create_schema = schemas.StoredFileCreate(user_id=random_uuid, path=path, content=content, name=file.filename, size=file.size)
    stored_file = await StoredFile.create(session, schema=create_schema)
    return {'ok': True, 'id': stored_file.id}