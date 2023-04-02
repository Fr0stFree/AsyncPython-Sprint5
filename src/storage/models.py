from uuid import uuid4
import datetime as dt

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from base.database import Base
from . import constants


class StoredFile(Base):
    __tablename__ = 'stored_file'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    path = Column(String, unique=True, nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='files')
    name = Column(String(constants.MAX_FILE_NAME_LENGTH), nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    is_private = Column(Boolean, nullable=False, default=False)
    size = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'<StoredFile (id={self.id}, path={self.path}, size={self.size} bytes, created_at={self.created_at})>'

    def __str__(self) -> str:
        return self.path
