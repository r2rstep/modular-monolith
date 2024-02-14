from abc import ABC
from typing import TypeVar

from building_blocks.event import Event


class DomainEvent(ABC, Event):
    ...


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)
