import os
from pathlib import Path
from pydantic import Field, AnyUrl, PostgresDsn, root_validator
from pydantic_settings import BaseSettings
from typing import Dict, Any

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "menu-project"
    PROJECT_VERSION: str = "1.0.0"

    DOMAIN: AnyUrl = "https://127.0.0.1:8000/"
    POSTGRES_PASSWORD: str = Field(env="POSTGRES_PASSWORD")
    POSTGRES_USER: str = Field(env="POSTGRES_USER")
    POSTGRES_SERVER: str = Field(env="POSTGRES_SERVER")
    POSTGRES_PORT: int = Field(env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(env="POSTGRES_DB")
    DATABASE_URL: PostgresDsn

    @root_validator(pre=True)
    def assemble_dsn(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["DATABASE_URL"] = PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_SERVER"],
            port=int(values["POSTGRES_PORT"]),
            path=values['POSTGRES_DB'],
        )
        return values


settings = Settings()
