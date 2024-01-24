from typing import cast

import injector

from modules.rich_domain.module_1.core.application.event_handlers.rich_domain_model_created_handler import (
    RichDomainModelCreatedHandler,
)
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.application.generic_event_handlers import GenericStorePublicEventInOutbox
from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    DomainEventType,
    event_originates_from_module,
    is_public_event,
)
from infrastructure.event_bus import EventBus, EventHandlingMediatorBase, EventsSubscriptionsConfiguratorBase
from modules.rich_domain.module_1.infrastructure import settings


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
            (RichDomainModelCreated, RichDomainModelCreatedHandler),
        ]:
            event_bus.subscribe(event_cls, cast(type[DomainEventHandler[DomainEvent]], handler_cls), mediator)
            if is_public_event(event_cls) and event_originates_from_module(event_cls, settings.MODULE):
                event_bus.subscribe(event_cls, GenericStorePublicEventInOutbox, mediator)
