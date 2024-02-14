from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union, overload

import injector

from building_blocks.application.event_handlers import (
    DomainEventHandler,
    EventHandlerType,
    EventType,
    IntegrationEventHandler,
    NotificationEventHandler,
)
from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent, NotificationEventType
from building_blocks.domain.event import DomainEvent, DomainEventType


class Subscriptions(dict[type[EventType], list[EventHandlerType]]):
    ...


class EventBus:
    @injector.inject
    def __init__(self) -> None:
        self._subscriptions: Union[
            Subscriptions[DomainEvent, DomainEventHandler[DomainEvent]],
            Subscriptions[NotificationEvent, NotificationEventHandler[NotificationEvent]],
        ] = defaultdict(list)  # type: ignore[assignment]

    @overload
    def subscribe(
        self,
        event_cls: type[DomainEventType],
        handler: DomainEventHandler[DomainEventType],
    ) -> None:
        ...

    @overload
    def subscribe(
        self,
        event_cls: type[NotificationEventType],
        handler: NotificationEventHandler[NotificationEventType],
    ) -> None:
        ...

    @overload
    def subscribe(
        self,
        event_cls: type[IntegrationEvent],
        handler: IntegrationEventHandler[IntegrationEvent],
    ) -> None:
        ...

    def subscribe(self, event_cls, handler):  # type: ignore[no-untyped-def]
        self._subscriptions[event_cls].append(handler)

    @overload
    async def publish(self, event: DomainEvent) -> None:
        ...

    @overload
    async def publish(self, event: NotificationEvent) -> None:
        ...

    @overload
    async def publish(self, event: IntegrationEvent) -> None:
        ...

    async def publish(self, event):  # type: ignore[no-untyped-def]
        handlers = self._subscriptions.get(type(event))
        if handlers:
            for handler in handlers:
                await handler.handle(event)


class EventsSubscriptionsConfiguratorBase(ABC):
    @abstractmethod
    def configure_subscriptions(self) -> None:
        ...
