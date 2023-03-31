from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship

from base.database import Base
from .settings import settings


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    files = relationship('StoredFile', back_populates='user', cascade='all, delete-orphan')
    username = Column(String(settings.MAX_USERNAME_LENGTH),
                      CheckConstraint(f'length(username) > {settings.MIN_USERNAME_LENGTH}'),
                      nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __repr__(self) -> str:
        return f'<User (id={self.id}, username={self.username})>'

    def __str__(self) -> str:
        return self.username
