from abc import ABC
from datetime import datetime
from typing import TypeVar

from pydantic import ConfigDict, Field
from pydantic.fields import FieldInfo

from building_blocks.event import Event


# pydantic features are not really needed but for sake of better DevEx it's better to have all the events technicalities
# handled the same way
class DomainEvent(ABC, Event):
    is_public: bool = False
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @classmethod
    def event_name(cls) -> str:
        return f"{DomainEvent.__name__}__{cls.__name__}"


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)


def is_public_event(event_cls: type[DomainEvent]) -> bool:
    return bool(event_cls.model_fields.get("is_public", FieldInfo(default=True)).default)


def event_originates_from_module(event_cls: type[DomainEvent], module_path: str) -> bool:
    return event_cls.__module__.startswith(module_path)
