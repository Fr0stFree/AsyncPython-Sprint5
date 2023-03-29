from pydantic import BaseSettings


class Settings(BaseSettings):
    MIN_USERNAME_LENGTH: int = 5
    MAX_USERNAME_LENGTH: int = 20

    MIN_PASSWORD_LENGTH: int = 8
    MAX_PASSWORD_LENGTH: int = 20

    HASH_ALGORITHM: str = "HS256"
    TOKEN_EXPIRES_AFTER: int = 60 * 60 * 24  # 1 day


settings = Settings()
