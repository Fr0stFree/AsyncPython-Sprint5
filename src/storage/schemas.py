from uuid import UUID
from pathlib import PosixPath
import datetime as dt
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field

from .settings import settings


class StoredFileBase(BaseModel):
    pass


class StoredFileCreate(BaseModel):
    path: PosixPath = Field(..., description="File path")
    is_private: bool = Field(default=False, description="If true, only the owner can access the file")
    user_id: UUID
    content: bytes
    name: str = Field(..., description="File name")
    size: int = Field(..., description="File size in bytes")


class StoredFileUpdate(StoredFileBase):
    user_id: UUID = Field(exclude=True)


class StoredFileCreatedResponse(BaseModel):
    id: UUID
    name: str
    path: PosixPath
    created_at: dt.datetime
    is_private: bool

    class Config:
        orm_mode = True