from abc import ABC, abstractmethod

from building_blocks.within_bounded_context.domain.events import DomainEvent


class DomainEventHandler(ABC):
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        ...
