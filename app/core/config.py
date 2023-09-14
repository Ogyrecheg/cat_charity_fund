from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Пожертвования котикам'
    description: str = 'Описание сервиса пожертвований котикам'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
