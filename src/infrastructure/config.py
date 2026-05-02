from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from src.domain.exceptions import ConfigError
from pathlib import Path

import os

path_to_env = Path(__file__).parents[2]


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    DEBUG: bool = False
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DB_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DB_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=f'{path_to_env}/.env')


class TestConfig:

    @property
    def DB_URL_psycopg(self):
        return 'sqlite:///:memory:'

    @property
    def DB_URL_asyncpg(self):
        return 'sqlite:///:memory:'


class LocalConfig(Settings):
    ENV: str = 'local'
    DEBUG: bool = True


class ProdConfig(Settings):
    ENV: str = 'prod'
    API_KEY: SecretStr


def get_config(cfg: str=os.getenv("APP_ENV", "local")):
    if cfg == 'local':
        return LocalConfig
    elif cfg == 'prod':
        return ProdConfig
    elif cfg == 'test':
        return TestConfig
    else:
        raise ConfigError(f'{cfg} не является предусмотренным конфигом')
