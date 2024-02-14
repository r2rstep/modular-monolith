from abc import ABC
from typing import TypeVar

from building_blocks.event import Event


class DomainEvent(ABC, Event):
    @classmethod
    def event_name(cls) -> str:
        return f"{DomainEvent.__name__}__{cls.__name__}"


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)
