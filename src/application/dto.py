from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict
from uuid import UUID
#from src.domain.entities import Status

class ResourceBaseDTO(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResourceCreateDTO(ResourceBaseDTO):
    pass


class ResourceUpdateDTO(ResourceBaseDTO):
    name: str | None = None
    metadata: Dict[str, Any] | None = None


class ResourceReadDTO(ResourceBaseDTO):
    id: UUID
    status: str

    model_config = ConfigDict(from_attributes=True)
