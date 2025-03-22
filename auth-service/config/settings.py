from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

BaseDir = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BaseDir / "certs" / "jwt-private.pem"
    public_key_path: Path = BaseDir / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:qwerty@localhost:5432/"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "qwerty"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = ""
    ECHO: bool = False

    auth: AuthJWT = AuthJWT()

    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/"


app_settings = Settings()
