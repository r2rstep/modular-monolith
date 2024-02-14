import injector

from modules.rich_domain.module_2.core.application.module_1_events_handlers import DoSomething
from modules.rich_domain.module_2.core.types import Module1

from commons.event_bus.application.event_bus import EventBus, EventsSubscriptionsConfiguratorBase
from commons.messagebox.application.generic_event_handlers import build_store_command_in_inbox_handler
from commons.messagebox.application.message_handlers import NotificationEventMessageHandler
from commons.messagebox.application.process_messagebox_handlers import ProcessOutboxHandler
from commons.messagebox.infrastructure.messagebox import MessageTopic


class EventsSubscriptionsConfigurator(EventsSubscriptionsConfiguratorBase):
    @injector.inject
    def __init__(
        self,
        container: injector.Injector,
        event_bus: EventBus,
        process_outbox_handler: ProcessOutboxHandler,
        module_1: Module1,
    ) -> None:
        self._container = container
        self._event_bus = event_bus
        self._process_outbox_handler = process_outbox_handler
        self._module_1 = module_1

    def configure_subscriptions(self) -> None:
        self._subscribe_notifications()

    def _subscribe_notifications(self) -> None:
        for notification_cls, handler_cls in [
            (
                self._module_1.RichDomainModelCreatedNotification,
                build_store_command_in_inbox_handler(DoSomething, self._module_1.RichDomainModelCreatedNotification),
            ),
        ]:
            self._event_bus.subscribe(notification_cls, self._container.get(handler_cls))

            self._process_outbox_handler.add_handler(
                MessageTopic(notification_cls.event_name()),
                NotificationEventMessageHandler(notification_cls, self._event_bus),
            )
