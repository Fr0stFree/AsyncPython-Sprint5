from http import HTTPStatus
from uuid import UUID
import pathlib
from fastapi import HTTPException, Form, UploadFile, File, Depends, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from base.database import get_session
from auth.dependencies import authentication
from .service import StoredFile
from .settings import settings


async def validated_file(user_id: UUID = Depends(authentication),
                         session: AsyncSession = Depends(get_session),
                         name: str = Form(None),
                         dir: str = Form(...),
                         is_private: bool = Form(False),
                         file: UploadFile = File(...)):
    if name is not None:
        file.filename = name
        
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                            detail=f'File size is too large. Max size is {settings.MAX_FILE_SIZE} bytes.')

    path = str(pathlib.PosixPath(dir, file.filename))
    if await StoredFile.filter(session, user_id=user_id, path=path):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="File already exists")

    file.path = path
    file.user_id = user_id
    file.is_private = is_private
    return file


async def existing_file(session: AsyncSession = Depends(get_session),
                        path: str = Query(None),
                        id: UUID = Query(None)):
    params = {'path': path, 'id': id}
    if path is None:
        params.pop('path')
    if id is None:
        params.pop('id')
    if not params:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Either path or id is required')

    try:
        stored_file = await StoredFile.get(session, **params)
    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='File not found')
    return stored_file
    

async def accessable_file(user_id: UUID = Depends(authentication),
                          stored_file: StoredFile = Depends(existing_file)) -> StoredFile:
    if stored_file.is_private and stored_file.user_id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail=f'File "{stored_file.name}" is private and you are not allowed to download it')
    return stored_file
