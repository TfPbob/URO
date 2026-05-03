from src.domain.interfaces import IUnitOfWork
from src.domain.entities import Resource
from src.domain.exceptions import ResourceNotFound
from uuid import UUID
from typing import List


class ResourceService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_resource(self, name: str, metadata: dict):
        with self.uow:
            resource = Resource(name=name, metadata=metadata)
            self.uow.resources.add(resource)
            self.uow.commit()
            return resource

    def get_resource(self, resource_id: UUID) -> Resource:
        with self.uow:
            resource = self.uow.resources.get_by_id(resource_id)
            if resource:
                return resource
            else:
                raise ResourceNotFound(f'Ресурс не найден в репозитории')

    def activate_resource(self, resource_id: UUID) -> None:
        with self.uow:
            obj = self.uow.resources.get_by_id(resource_id)
            if obj is not None:
                obj.activate()
                self.uow.resources.update(obj)
                self.uow.commit()
            else:
                self.uow.rollback()
                raise ResourceNotFound(f'Ресурс не найден в репозитории')

    def list_all_resources(self) -> List[Resource]:
        with self.uow:
            return self.uow.resources.list_all()
