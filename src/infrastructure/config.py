import enum

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from src.domain.exceptions import ConfigError
from pathlib import Path


path_to_env = Path(__file__).parents[2]


class ConfigStatus(enum.Enum):
    local = 'local'
    test = 'test'
    prod = 'prod'

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
        return 'sqlite:///./test.db'

    @property
    def DB_URL_asyncpg(self):
        return 'sqlite:///./test.db'


class LocalConfig(Settings):
    ENV: str = 'local'
    DEBUG: bool = True


class ProdConfig(Settings):
    ENV: str = 'prod'
    API_KEY: SecretStr


def get_config(cfg: ConfigStatus):
    if cfg == ConfigStatus.local:
        return LocalConfig()
    elif cfg == ConfigStatus.prod:
        return ProdConfig()
    elif cfg == ConfigStatus.test:
        return TestConfig()
    else:
        raise ConfigError(f'{cfg} не является предусмотренным конфигом')
