from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    db_echo: bool = True #SQLAlchemy echo queries
    
    @property
    def DATABASE_URL_asyncpg(self):
        url = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        print(url)
        return url

    @property
    def DATABASE_URL_psycopg(self):
        url = f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        print(url)
        return url

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()