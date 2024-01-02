from collections import defaultdict
from typing import NewType

from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    DomainEventHandler,
)

Subscriptions = NewType("Subscriptions", dict[type[DomainEvent], list[type[DomainEventHandler]]])


class EventBus:
    def __init__(self) -> None:
        self.subscriptions: Subscriptions = defaultdict(list)

    def subscribe(self, event_cls: type[DomainEvent], handler_cls: type[DomainEventHandler]) -> None:
        self.subscriptions[event_cls].append(handler_cls)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self.subscriptions.get(type(event))
        if handlers:
            for handler_cls in handlers:
                handler = handler_cls()
                await handler.handle(event)
