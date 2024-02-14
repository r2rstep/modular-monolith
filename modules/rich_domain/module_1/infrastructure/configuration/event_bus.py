import injector

from modules.rich_domain.module_1.core.application.event_handlers.rich_domain_model_created_handler import (
    PublishRichDomainModelCreatedIntegrationEvent,
    RichDomainModelCreatedHandler,
)
from modules.rich_domain.module_1.core.application.events import RichDomainModelCreatedNotification
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from commons.event_bus.application.event_bus import EventBus, EventsSubscriptionsConfiguratorBase
from commons.messagebox.application.generic_event_handlers import build_store_notification_in_outbox_handler
from commons.messagebox.application.message_handlers import NotificationEventMessageHandler
from commons.messagebox.application.process_messagebox_handlers import ProcessOutboxHandler
from commons.messagebox.infrastructure.messagebox import MessageTopic


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
        for domain_event_cls, handler_cls, notification_event_cls in [
            (RichDomainModelCreated, RichDomainModelCreatedHandler, RichDomainModelCreatedNotification),
        ]:
            self._event_bus.subscribe(domain_event_cls, self._container.get(handler_cls))

            if notification_event_cls:  # type: ignore[truthy-function]
                self._event_bus.subscribe(
                    domain_event_cls,
                    self._container.get(
                        build_store_notification_in_outbox_handler(notification_event_cls, domain_event_cls)
                    ),
                )
                self._process_outbox_handler.add_handler(
                    MessageTopic(notification_event_cls.event_name()),
                    NotificationEventMessageHandler(notification_event_cls, self._event_bus),
                )

    def _subscribe_notification_events(self) -> None:
        self._event_bus.subscribe(
            RichDomainModelCreatedNotification,
            self._container.get(PublishRichDomainModelCreatedIntegrationEvent),
        )
