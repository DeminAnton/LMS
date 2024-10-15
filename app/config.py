from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent


class Prefix(BaseModel):
    api: str = "/api"

    
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    
class DatabaseConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    db_echo: bool = True  # SQLAlchemy echo queries
    db_echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 100

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def db_url_async(self):
        url = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url

    @property
    def db_url_sync(self):
        url = f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url


class Settings(BaseSettings):
    db_config: DatabaseConfig = DatabaseConfig()
    prefix: Prefix = Prefix()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
