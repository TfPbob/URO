import enum

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any, Dict
from src.domain.exceptions import StateError

class Status(enum.Enum):
    DRAFT = 'DRAFT'
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


@dataclass
class Resource:
    name: str
    status: str = Status.DRAFT.value
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)

    def activate(self):
        """Метод активации ресурса"""
        if self.status == Status.DRAFT.value:
            self.status = Status.ACTIVE.value
        elif self.status == Status.ACTIVE.value:
            return
        else:
            raise StateError(f'Нельзя активировать ресурс из состояния {self.status}')

    def delete(self):
        """Метод удаления ресурса"""
        self.status = Status.DELETED.value
