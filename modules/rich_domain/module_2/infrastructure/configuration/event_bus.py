import injector

from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.application.generic_event_handlers import (
    GenericStorePublicEventInOutbox,
    build_store_command_in_inbox_handler,
)
from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    event_originates_from_module,
    is_public_event,
)
from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus, EventHandlingMediatorBase
from modules.rich_domain.module_2.application.module_1_events_handlers import DoSomething
from modules.rich_domain.module_2.infrastructure import settings


class EventHandlingMediator(EventHandlingMediatorBase):
    @injector.inject
    def __init__(self, container: injector.Injector) -> None:
        self._container = container

    async def handle(self, event: DomainEvent, event_handler: type[DomainEventHandler]) -> None:
        await self._container.get(event_handler).handle(event)


@injector.inject
def configure_subscriptions(event_bus: EventBus, mediator: EventHandlingMediator) -> None:
    for event_cls, handler_cls in [
        (RichDomainModelCreated, build_store_command_in_inbox_handler(DoSomething)),
    ]:
        event_bus.subscribe(event_cls, handler_cls, mediator)
        if is_public_event(event_cls) and event_originates_from_module(event_cls, settings.MODULE):
            event_bus.subscribe(event_cls, GenericStorePublicEventInOutbox, mediator)
