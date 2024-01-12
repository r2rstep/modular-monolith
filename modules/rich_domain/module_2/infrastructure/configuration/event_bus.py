from typing import Union

import injector
from typing_extensions import TypeGuard

from modules.rich_domain.module_2.core.application.module_1_events_handlers import DoSomething

from building_blocks.within_bounded_context.application.notification_event import NotificationEvent
from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    DomainEventType,
    event_originates_from_module,
    is_public_event,
)
from commons.event_bus.application.event_bus import (
    EventBus,
    EventsSubscriptionsConfiguratorBase,
)
from commons.messagebox.application.generic_event_handlers import (
    GenericStoreNotificationEventInOutbox,
    build_store_command_in_inbox_handler,
)
from commons.messagebox.types import PublicDomainEventsClsList
from modules.rich_domain.module_1.interface import RichDomainModelCreated
from modules.rich_domain.module_2.infrastructure import settings


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
            (
                NotificationEvent[RichDomainModelCreated],
                build_store_command_in_inbox_handler(DoSomething, RichDomainModelCreated),
            ),
        ]:
            event_bus.subscribe(event_cls, self._container.get(handler_cls))
            if (
                self._is_domain_event(event_cls)
                and is_public_event(event_cls)
                and event_originates_from_module(event_cls, settings.MODULE)
            ):
                event_bus.subscribe(event_cls, self._container.get(GenericStoreNotificationEventInOutbox))
                public_domain_events_cls_list.append(event_cls)

    def _is_domain_event(
        self, event_cls: Union[type[DomainEventType], type[NotificationEvent[DomainEventType]]]
    ) -> TypeGuard[type[DomainEventType]]:
        return issubclass(event_cls, DomainEvent)
