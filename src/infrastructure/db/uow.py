from sqlalchemy.orm import sessionmaker
from src.domain.interfaces import IUnitOfWork
from src.infrastructure.db.repository import SQLAlchemyRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.resources: SQLAlchemyRepository | None = None

    def __enter__(self):
        self.session = self.session_factory()
        self.resources = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
