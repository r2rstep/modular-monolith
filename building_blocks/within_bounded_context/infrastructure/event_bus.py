from collections import defaultdict

from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    DomainEventHandler,
)


class EventBus:
    def __init__(self) -> None:
        self.subscriptions: dict[type[DomainEvent], list[type[DomainEventHandler]]] = defaultdict(list)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self.subscriptions.get(type(event))
        if handlers:
            for handler_cls in handlers:
                handler = handler_cls()
                await handler.handle(event)


def init_event_bus() -> EventBus:
    return EventBus()
