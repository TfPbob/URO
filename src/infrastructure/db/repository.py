from typing import List
from src.domain.interfaces import IResourceRepository
from sqlalchemy.orm.session import Session
from src.domain.entities import Resource
from src.infrastructure.db.models import ResourceModel
from uuid import UUID


class SQLAlchemyRepository(IResourceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Resource):
        obj = ResourceMapped.from_domain(entity)
        self.session.add(obj)

    def get_by_id(self, id: UUID) -> Resource | None:
        obj = self.session.get(ResourceModel, id)
        if obj:
            return ResourceMapped.to_domain(obj)
        else:
            return None

    def list_all(self) -> List[Resource]:
        list_all_object = self.session.query(ResourceModel).all()
        if list_all_object:
            return [ResourceMapped.to_domain(obj) for obj in list_all_object]
        else:
            return []

    def update(self, entity: Resource):
        model = self.session.query(ResourceModel).filter_by(id=entity.id).first()
        if model:
            model.status = entity.status
            model.name = entity.name
            model.id = entity.id
            model.resource_metadata = entity.metadata


class ResourceMapped:
    @staticmethod
    def to_domain(entity: ResourceModel) -> Resource:
        """Метод перехода к доменному ресурсу"""
        return Resource(
            id=entity.id,
            name=entity.name,
            status=entity.status,
            metadata=entity.resource_metadata,
        )
    @staticmethod
    def from_domain(entity: Resource):
        """Метод перехода из доменного ресурса к модели БД"""
        return ResourceModel(
            id=entity.id,
            name=entity.name,
            status=entity.status,
            metadata=entity.metadata
        )
