from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Async-Practicum-app'
    DEBUG: bool = Field(..., env='DEBUG')
    SERVER_PORT: int = Field(..., env='SERVER_PORT')
    SERVER_HOST: str = Field(..., env='SERVER_HOST')
    
    DB_HOST: str = Field(..., env='POSTGRES_HOST')
    DB_PORT: int = Field(..., env='POSTGRES_PORT')
    DB_NAME: str = Field(..., env='POSTGRES_DB')
    DB_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    DB_USER: str = Field(..., env='POSTGRES_USER')
    
    @property
    def database_dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(
            db=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )
    
    @property
    def server_address(self) -> str:
        return f'http://{self.SERVER_HOST}:{self.SERVER_PORT}'
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        

settings = Settings()
