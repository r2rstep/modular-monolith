import injector

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent
from building_blocks.within_bounded_context.infrastructure.messagebox import MessageName, Outbox


class GenericStorePublicEventInOutbox(DomainEventHandler):
    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        self._outbox = outbox

    async def handle(self, event: DomainEvent) -> None:
        if event.is_public:
            await self._outbox.add(MessageName(event.name), dict(event))
