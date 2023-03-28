from pydantic import BaseSettings


class Settings(BaseSettings):
    MIN_USERNAME_LENGTH: int = 5
    MAX_USERNAME_LENGTH: int = 20

    MIN_PASSWORD_LENGTH: int = 8
    MAX_PASSWORD_LENGTH: int = 20


settings = Settings()
