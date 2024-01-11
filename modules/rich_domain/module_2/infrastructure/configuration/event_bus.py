import injector

from modules.rich_domain.module_2.core.application.module_1_events_handlers import DoSomething

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import (
    DomainEventType,
    event_originates_from_module,
    is_public_event,
)
from commons.event_bus.application.event_bus import (
    EventBus,
    EventHandlingMediatorBase,
    EventsSubscriptionsConfiguratorBase,
)
from commons.messagebox.application.generic_event_handlers import (
    GenericStorePublicEventInOutbox,
    build_store_command_in_inbox_handler,
)
from modules.rich_domain.module_1.interface import RichDomainModelCreated
from modules.rich_domain.module_2.infrastructure import settings


class EventHandlingMediator(EventHandlingMediatorBase):
    @injector.inject
    def __init__(self, container: injector.Injector) -> None:
        self._container = container

    async def handle(self, event: DomainEventType, event_handler: type[DomainEventHandler[DomainEventType]]) -> None:
        await self._container.get(event_handler).handle(event)


class EventsSubscriptionsConfigurator(EventsSubscriptionsConfiguratorBase):
    @injector.inject
    def configure_subscriptions(self, event_bus: EventBus, mediator: EventHandlingMediatorBase) -> None:
        for event_cls, handler_cls in [
            (RichDomainModelCreated, build_store_command_in_inbox_handler(DoSomething)),
        ]:
            event_bus.subscribe(event_cls, handler_cls, mediator)
            if is_public_event(event_cls) and event_originates_from_module(event_cls, settings.MODULE):
                event_bus.subscribe(event_cls, GenericStorePublicEventInOutbox, mediator)
