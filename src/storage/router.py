from http import HTTPStatus
from uuid import UUID
import io

from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import authentication
from base.database import get_session
from . import schemas
from .service import StoredFile
from .dependencies import validated_file, accessable_file


router = APIRouter(prefix="/storage", tags=["storage"], dependencies=[Depends(authentication)])


@router.post('/upload', status_code=HTTPStatus.CREATED)
async def upload_file(background_tasks: BackgroundTasks,
                      file: UploadFile = Depends(validated_file),
                      session: AsyncSession = Depends(get_session)) -> schemas.StoredFileDB:
    stored_file = await StoredFile.upload(session, file, background_tasks)
    return stored_file


@router.get('/')
async def list_files(user_id: UUID = Depends(authentication),
                     session: AsyncSession = Depends(get_session)) -> list[schemas.StoredFileDB]:
    files = await StoredFile.filter(session, user_id=user_id)
    return files


@router.get('/download')
async def download_file(stored_file: StoredFile = Depends(accessable_file)) -> StreamingResponse:
    content = await StoredFile.download(stored_file)
    return StreamingResponse(io.BytesIO(content), media_type='application/octet-stream')
