from base.service import RepositoryInterface

from .models import StoredFile as StoredFileModel
from .schemas import StoredFileCreate, StoredFileUpdate


class StoredFileRepository(RepositoryInterface[StoredFileModel, StoredFileCreate, StoredFileUpdate]):
    pass


StoredFile = StoredFileRepository(StoredFileModel)
