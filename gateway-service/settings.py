from pathlib import Path

from pydantic_settings import BaseSettings

BaseDir = Path(__file__).parent.parent


class Settings(BaseSettings):
    AMQP_URL: str = 'amqp://guest:guest@localhost:5672'
    SMART_HOME_SERVICE_URL: str = 'http://localhost:8006'


app_settings = Settings()
