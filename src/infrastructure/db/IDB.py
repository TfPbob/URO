from src.infrastructure.config import ConfigStatus, get_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.infrastructure.db.models import Base


class InfrastructureDB:
    _instance = None
    def __new__(cls, cfg: ConfigStatus):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            url = get_config(cfg).DB_URL_psycopg
            cls._instance.engine = create_engine(
                url,
                connect_args={"check_same_thread": False},
                echo=True,
                pool_size=10,
                pool_pre_ping=True,
            )
            cls._instance.SessionLocal = sessionmaker(bind=cls._instance.engine)
        return cls._instance

    def init_db(self):
        print(f"Таблицы в метаданных: {Base.metadata.tables.keys()}")
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()
