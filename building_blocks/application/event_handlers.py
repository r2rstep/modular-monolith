from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from building_blocks.application.integration_event import IntegrationEvent, IntegrationEventType
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent, DomainEventType


class DomainEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: DomainEventType) -> None:
        ...


class NotificationEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: NotificationEvent[DomainEventType]) -> None:
        ...


class IntegrationEventHandler(ABC, Generic[IntegrationEventType]):
    @abstractmethod
    async def handle(self, event: IntegrationEventType) -> None:
        ...


EventType = TypeVar("EventType", DomainEvent, NotificationEvent[DomainEvent], IntegrationEvent)
EventHandlerType = TypeVar(
    "EventHandlerType",
    DomainEventHandler[DomainEvent],
    NotificationEventHandler[DomainEvent],
    IntegrationEventHandler[IntegrationEvent],
)
