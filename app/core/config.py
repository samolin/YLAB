from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class App(BaseSettings):
    PROJECT_NAME: str = 'menu-project'
    PROJECT_VERSION: str = '1.0.0'


class Postgres(BaseSettings):

    DOMAIN: str = 'https://127.0.0.1:8000/'
    POSTGRES_PASSWORD: str = Field(env='POSTGRES_PASSWORD')
    POSTGRES_USER: str = Field(env='POSTGRES_USER')
    POSTGRES_SERVER: str = Field(env='POSTGRES_SERVER')
    POSTGRES_PORT: int = Field(env='POSTGRES_PORT')
    POSTGRES_DB: str = Field(env='POSTGRES_DB')
    DATABASE_URL: PostgresDsn

    @model_validator(mode='before')
    def assemble_dsn(cls, values: dict[str, Any]) -> dict[str, Any]:
        values['DATABASE_URL'] = PostgresDsn.build(
            scheme='postgresql+psycopg2',
            username=values['POSTGRES_USER'],
            password=values['POSTGRES_PASSWORD'],
            host=values['POSTGRES_SERVER'],
            port=int(values['POSTGRES_PORT']),
            path=values['POSTGRES_DB'],
        )
        return values


class Redis(BaseSettings):
    REDIS_HOST: str = Field(env='REDIS_HOST')
    REDIS_PORT: int = Field(env='REDIS_PORT')
    REDIS_DB: str = Field(env='REDIS_DB')
    REDIS_URL: RedisDsn

    @model_validator(mode='before')
    def assemble_dsn(cls, values: dict[str, Any]) -> dict[str, Any]:
        values['REDIS_URL'] = RedisDsn.build(
            scheme='redis',
            host=values['REDIS_HOST'],
            port=int(values['REDIS_PORT']),
            path=f"/{values['REDIS_DB']}",
        )
        return values


class Settings(BaseSettings):
    app: App = App()
    postgres: Postgres = Postgres()
    redis: Redis = Redis()


settings = Settings()
