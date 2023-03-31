from pydantic import BaseSettings


class Settings(BaseSettings):
    MIN_FILE_NAME_LENGTH: int = 3
    MAX_FILE_NAME_LENGTH: int = 35

    MAX_FILE_SIZE: int = 1024 * 1024 * 10  # 10 MB


settings = Settings()
