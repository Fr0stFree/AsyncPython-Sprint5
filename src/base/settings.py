from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = 'Zephyr'
    secret_key: str = Field(..., env='SECRET_KEY')
    debug: bool = Field(..., env='DEBUG')
    server_port: int = Field(..., env='SERVER_PORT')
    server_host: str = Field(..., env='SERVER_HOST')

    db_host: str = Field(..., env='POSTGRES_HOST')
    db_port: int = Field(..., env='POSTGRES_PORT')
    db_name: str = Field(..., env='POSTGRES_DB')
    db_password: str = Field(..., env='POSTGRES_PASSWORD')
    db_user: str = Field(..., env='POSTGRES_USER')

    @property
    def database_dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(
            db=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
        )

    @property
    def server_address(self) -> str:
        return f'http://{self.server_host}:{self.server_port}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
