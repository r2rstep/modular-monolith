import injector

from modules.rich_domain.module_1.core.application.event_handlers.rich_domain_model_created_handler import (
    RichDomainModelCreatedHandler,
)
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    event_originates_from_module,
    is_public_event,
)
from commons.event_bus.application.event_bus import (
    EventBus,
    EventsSubscriptionsConfiguratorBase,
)
from commons.messagebox.application.generic_event_handlers import GenericStoreNotificationEventInOutbox
from commons.messagebox.types import PublicDomainEventsClsList
from modules.rich_domain.module_1.infrastructure import settings


class EventsSubscriptionsConfigurator(EventsSubscriptionsConfiguratorBase):
    @injector.inject
    def __init__(self, container: injector.Injector) -> None:
        self._container = container

    @injector.inject
    def configure_subscriptions(
        self,
        event_bus: EventBus,
        public_domain_events_cls_list: PublicDomainEventsClsList,
    ) -> None:
        for event_cls, handler_cls in [
            (RichDomainModelCreated, RichDomainModelCreatedHandler),
        ]:
            event_bus.subscribe(event_cls, self._container.get(handler_cls))
            if (
                issubclass(event_cls, DomainEvent)
                and is_public_event(event_cls)
                and event_originates_from_module(event_cls, settings.MODULE)
            ):
                event_bus.subscribe(event_cls, self._container.get(GenericStoreNotificationEventInOutbox))
                public_domain_events_cls_list.append(event_cls)
