import enum

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any, Dict
from exceptions import StateError

class Status(enum.Enum):
    DRAFT = 'Draft'
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


@dataclass
class Resource:
    name: str
    status: Status = Status.DRAFT
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)

    def activate(self):
        """Метод активации ресурса"""
        if self.status == Status.DRAFT:
            self.status = Status.ACTIVE
        elif self.status == Status.ACTIVE:
            return
        else:
            raise StateError(f'Нельзя активировать ресурс из состояния {self.status}')

    def delete(self):
        """Метод удаления ресурса"""
        self.status = Status.DELETED
