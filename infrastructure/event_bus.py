from abc import ABC, abstractmethod
from collections import defaultdict
from typing import NewType

import injector

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
)

Subscriptions = NewType(
    "Subscriptions", dict[type[DomainEvent], list[tuple[type[DomainEventHandler], "EventHandlingMediatorBase"]]]
)


class EventBus:
    @injector.inject
    def __init__(self) -> None:
        self._subscriptions: Subscriptions = defaultdict(list)

    def subscribe(
        self, event_cls: type[DomainEvent], handler_cls: type[DomainEventHandler], mediator: "EventHandlingMediatorBase"
    ) -> None:
        self._subscriptions[event_cls].append((handler_cls, mediator))

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._subscriptions.get(type(event))
        if handlers:
            for handler_cls, mediator in handlers:
                await mediator.handle(event, handler_cls)


class EventHandlingMediatorBase(ABC):
    """
    Enables injecting module specific dependencies into event handlers.
    """

    @abstractmethod
    async def handle(self, event: DomainEvent, handler_cls: type[DomainEventHandler]) -> None:
        ...


class EventsSubscriptionsConfiguratorBase(ABC):
    @abstractmethod
    def configure_subscriptions(self, event_bus: EventBus, mediator: EventHandlingMediatorBase) -> None:
        ...
