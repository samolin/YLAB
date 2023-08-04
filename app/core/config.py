from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import AnyUrl, Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'menu-project'
    PROJECT_VERSION: str = '1.0.0'

    DOMAIN: AnyUrl = 'https://127.0.0.1:8000/'
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


settings = Settings()
