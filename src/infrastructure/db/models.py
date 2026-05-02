from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import JSON, String
from uuid import UUID, uuid4
from src.domain.entities import Status


class Base(DeclarativeBase):
    pass


class ResourceModel(Base):
    __tablename__ = 'resources'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[Status] = mapped_column(String(64), nullable=False, default=Status.DRAFT)
    resource_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
