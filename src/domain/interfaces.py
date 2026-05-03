from abc import abstractmethod, ABC
from src.domain.entities import Resource
from typing import List, Optional
from uuid import UUID
from dataclasses import dataclass


class IResourceRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[Resource]:
        pass

    @abstractmethod
    def add(self, entity: Resource) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Resource]:
        pass

    @abstractmethod
    def update(self, eninte: Resource) -> None:
        pass


@dataclass
class IUnitOfWork(ABC):
    resources: IResourceRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
