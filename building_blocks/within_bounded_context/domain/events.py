from abc import ABC
from datetime import datetime
from typing import TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo, PrivateAttr


# pydantic features are not really needed but for sake of better DevEx it's better to have all the events technicalities
# handled the same way
class DomainEvent(ABC, BaseModel):
    _pk: UUID = PrivateAttr(default_factory=uuid4)
    is_public: bool = False
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def idempotence_id(self) -> str:
        return f"{self.name}_{self._pk}"


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)


def is_public_event(event_cls: type[DomainEvent]) -> bool:
    return event_cls.model_fields.get("is_public", FieldInfo(default=True)).default


def event_originates_from_module(event_cls: type[DomainEvent], module_path: str) -> bool:
    return event_cls.__module__.startswith(module_path)
