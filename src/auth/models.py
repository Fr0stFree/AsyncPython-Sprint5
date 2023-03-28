from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from base.database import Base
from .settings import settings


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(settings.MAX_USERNAME_LENGTH), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    
    __table_args__ = (
        CheckConstraint(f'length(username) > {settings.MIN_USERNAME_LENGTH}'),
    )
    
    
    
