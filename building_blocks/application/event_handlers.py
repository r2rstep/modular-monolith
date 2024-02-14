from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from building_blocks.application.integration_event import IntegrationEvent, IntegrationEventType
from building_blocks.application.notification_event import NotificationEvent, NotificationEventType
from building_blocks.domain.event import DomainEvent, DomainEventType


class DomainEventHandler(ABC, Generic[DomainEventType]):
    @abstractmethod
    async def handle(self, event: DomainEventType) -> None:
        ...


class NotificationEventHandler(ABC, Generic[NotificationEventType]):
    @abstractmethod
    async def handle(self, event: NotificationEventType) -> None:
        ...


class IntegrationEventHandler(ABC, Generic[IntegrationEventType]):
    @abstractmethod
    async def handle(self, event: IntegrationEventType) -> None:
        ...


EventType = TypeVar("EventType", DomainEvent, NotificationEvent, IntegrationEvent)
EventHandlerType = TypeVar(
    "EventHandlerType",
    DomainEventHandler[DomainEvent],
    NotificationEventHandler[NotificationEvent],
    IntegrationEventHandler[IntegrationEvent],
)
