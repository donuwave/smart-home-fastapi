from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

BaseDir = Path(__file__).parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:qwerty@localhost:5434/"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5434"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "qwerty"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = ""
    ECHO: bool = False
    AMQP_URL: str = 'amqp://guest:guest@localhost:5672'

    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/"


app_settings = Settings()
