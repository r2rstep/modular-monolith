from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union, overload

import injector

from building_blocks.within_bounded_context.application.event_handlers import (
    DomainEventHandler,
    EventHandlerType,
    EventType,
    NotificationEventHandler,
)
from building_blocks.within_bounded_context.application.notification_event import NotificationEvent
from building_blocks.within_bounded_context.domain.events import DomainEvent, DomainEventType
from commons.messagebox.types import PublicDomainEventsClsList


class Subscriptions(dict[type[EventType], list[EventHandlerType]]):
    ...


class EventBus:
    @injector.inject
    def __init__(self) -> None:
        self._subscriptions: Union[
            Subscriptions[DomainEvent, DomainEventHandler[DomainEvent]],
            Subscriptions[NotificationEvent[DomainEvent], NotificationEventHandler[DomainEvent]],
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
        event_cls: type[NotificationEvent[DomainEventType]],
        handler: NotificationEventHandler[DomainEventType],
    ) -> None:
        ...

    def subscribe(self, event_cls, handler):  # type: ignore[no-untyped-def]
        self._subscriptions[event_cls].append(handler)

    @overload
    async def publish(self, event: DomainEvent) -> None:
        ...

    @overload
    async def publish(self, event: NotificationEvent[DomainEvent]) -> None:
        ...

    async def publish(self, event):  # type: ignore[no-untyped-def]
        handlers = self._subscriptions.get(type(event))
        if handlers:
            for handler in handlers:
                await handler.handle(event)


class EventsSubscriptionsConfiguratorBase(ABC):
    @abstractmethod
    def configure_subscriptions(
        self,
        event_bus: EventBus,
        public_domain_events_cls_list: PublicDomainEventsClsList,
    ) -> None:
        ...
