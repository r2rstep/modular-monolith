from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from building_blocks.within_bounded_context.domain.events import DomainEvent

DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: DomainEventType) -> None:
        ...
