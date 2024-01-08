import injector

from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated
from modules.rich_domain.module_1.core.event_handlers.rich_domain_model_created_handler import (
    RichDomainModelCreatedHandler,
)

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.application.generic_event_handlers import GenericStorePublicEventInOutbox
from building_blocks.within_bounded_context.domain.events import DomainEvent, is_public_event
from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus, EventHandlingMediatorBase


class EventHandlingMediator(EventHandlingMediatorBase):
    @injector.inject
    def __init__(self, container: injector.Injector) -> None:
        self._container = container

    async def handle(self, event: DomainEvent, event_handler: type[DomainEventHandler]) -> None:
        await self._container.get(event_handler).handle(event)


@injector.inject
def configure_subscriptions(event_bus: EventBus, mediator: EventHandlingMediator) -> None:
    for event_cls, handler_cls in [
        (RichDomainModelCreated, RichDomainModelCreatedHandler),
    ]:
        event_bus.subscribe(event_cls, handler_cls, mediator)
        if is_public_event(event_cls):
            event_bus.subscribe(event_cls, GenericStorePublicEventInOutbox, mediator)
