import injector

from modules.rich_domain.module_1.core.application.event_handlers.rich_domain_model_created_handler import (
    PublishRichDomainModelCreatedIntegrationEvent,
    RichDomainModelCreatedHandler,
)
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import event_originates_from_module, is_public_event
from commons.event_bus.application.event_bus import EventBus, EventsSubscriptionsConfiguratorBase
from commons.messagebox.application.generic_event_handlers import GenericStoreNotificationEventInOutbox
from commons.messagebox.application.message_handlers import NotificationEventMessageHandler
from commons.messagebox.application.process_messagebox_handlers import ProcessOutboxHandler
from commons.messagebox.infrastructure.messagebox import MessageTopic
from modules.rich_domain.module_1.infrastructure import settings


class EventsSubscriptionsConfigurator(EventsSubscriptionsConfiguratorBase):
    @injector.inject
    def __init__(
        self, container: injector.Injector, event_bus: EventBus, process_outbox_handler: ProcessOutboxHandler
    ) -> None:
        self._container = container
        self._event_bus = event_bus
        self._process_outbox_handler = process_outbox_handler

    def configure_subscriptions(self) -> None:
        self._subscribe_domain_events()
        self._subscribe_notification_events()

    def _subscribe_domain_events(self) -> None:
        for event_cls, handler_cls in [
            (RichDomainModelCreated, RichDomainModelCreatedHandler),
        ]:
            self._event_bus.subscribe(event_cls, self._container.get(handler_cls))

            if is_public_event(event_cls) and event_originates_from_module(event_cls, settings.MODULE):
                self._event_bus.subscribe(event_cls, self._container.get(GenericStoreNotificationEventInOutbox))
                self._process_outbox_handler.add_handler(
                    MessageTopic(event_cls.event_name()), NotificationEventMessageHandler(event_cls, self._event_bus)
                )

    def _subscribe_notification_events(self) -> None:
        self._event_bus.subscribe(
            NotificationEvent[RichDomainModelCreated],
            self._container.get(PublishRichDomainModelCreatedIntegrationEvent),
        )
