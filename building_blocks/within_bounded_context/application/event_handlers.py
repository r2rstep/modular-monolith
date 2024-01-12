from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from building_blocks.within_bounded_context.application.notification_event import NotificationEvent
from building_blocks.within_bounded_context.domain.events import DomainEvent, DomainEventType


class DomainEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: DomainEventType) -> None:
        ...


class NotificationEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: NotificationEvent[DomainEventType]) -> None:
        ...


EventType = TypeVar("EventType", DomainEvent, NotificationEvent[DomainEvent])
EventHandlerType = TypeVar("EventHandlerType", DomainEventHandler[DomainEvent], NotificationEventHandler[DomainEvent])
