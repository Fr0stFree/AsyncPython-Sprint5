from uuid import uuid4
import datetime as dt

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, LargeBinary, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import CheckConstraint

from base.database import Base


from .settings import settings


class StoredFile(Base):
    __tablename__ = 'stored_file'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    user = relationship('User', back_populates='files')
    content = Column(LargeBinary, CheckConstraint(f'length(content) < {settings.MAX_FILE_SIZE}'), nullable=False)
    name = Column(String(settings.MAX_FILE_NAME_LENGTH),
                  CheckConstraint(f'length(name) > {settings.MIN_FILE_NAME_LENGTH}'), nullable=False)
    path = Column(String, nullable=False, index=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    is_private = Column(Boolean, nullable=False, default=False)
    size = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'<StoredFile (id={self.id}, path={self.path}, size={self.size} bytes, created_at={self.created_at})>'

    def __str__(self) -> str:
        return self.path
