from collections import defaultdict
from typing import NewType

import injector

from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
)
from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.infrastructure.messagebox import Outbox, MessageName

Subscriptions = NewType("Subscriptions", dict[type[DomainEvent], list[type[DomainEventHandler]]])


class EventBus:
    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        self._subscriptions: Subscriptions = defaultdict(list)
        self._outbox = outbox

    def subscribe(self, event_cls: type[DomainEvent], handler_cls: type[DomainEventHandler]) -> None:
        self._subscriptions[event_cls].append(handler_cls)

    async def publish(self, event: DomainEvent) -> None:
        if event.is_public:
            await self._outbox.add(MessageName(event.name), dict(event))

        handlers = self._subscriptions.get(type(event))
        if handlers:
            for handler_cls in handlers:
                handler = handler_cls()
                await handler.handle(event)
