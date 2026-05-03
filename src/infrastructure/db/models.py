from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import JSON, String
from uuid import UUID, uuid4
from src.domain.entities import Status


Base = declarative_base()


class ResourceModel(Base):
    __tablename__ = 'resources'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default=Status.DRAFT.value)
    resource_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
