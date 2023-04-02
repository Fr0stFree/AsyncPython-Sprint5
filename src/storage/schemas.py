import datetime as dt
from uuid import UUID

from pydantic import BaseModel


class StoredFileBase(BaseModel):
    pass


class StoredFileCreate(BaseModel):
    path: str
    user_id: UUID
    name: str
    size: int
    is_private: bool = False
    

class StoredFileUpdate(BaseModel):
    pass


class StoredFileDB(BaseModel):
    id: UUID
    name: str
    path: str
    user_id: UUID
    created_at: dt.datetime
    is_private: bool
    size: int

    class Config:
        orm_mode = True
