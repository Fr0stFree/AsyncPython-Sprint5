from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from botocore.client import BaseClient

from base.service import RepositoryInterface
from .client import get_client_session
from .models import StoredFile as StoredFileModel
from .schemas import StoredFileCreate, StoredFileUpdate
from . import constants


class StoredFileRepository(RepositoryInterface[StoredFileModel, StoredFileCreate, StoredFileUpdate]):
    async def upload(self, session: AsyncSession,
                     file: UploadFile,
                     background_tasks: BackgroundTasks,
                     client_session: BaseClient = get_client_session()) -> StoredFileModel:
        
        content = await file.read()
        stored_file = await super().create(session, StoredFileCreate(user_id=file.user_id,
                                                                     path=file.path, name=file.filename,
                                                                     size=file.size, is_private=file.is_private))
        background_tasks.add_task(func=client_session.put_object,
                                  Bucket=constants.BUCKET_NAME,
                                  Key=str(stored_file.id),
                                  Body=content)
        return stored_file

    async def download(self, stored_file: StoredFileModel,
                       client_session: BaseClient = get_client_session()) -> bytes:
        get_object_response = client_session.get_object(Bucket=constants.BUCKET_NAME, Key=str(stored_file.id))
        return get_object_response['Body'].read()


StoredFile = StoredFileRepository(StoredFileModel)
