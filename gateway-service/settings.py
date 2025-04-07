from pathlib import Path

from pydantic_settings import BaseSettings

BaseDir = Path(__file__).parent.parent


class Settings(BaseSettings):
    AMQP_URL: str = 'amqp://guest:guest@localhost:5672'

app_settings = Settings()
