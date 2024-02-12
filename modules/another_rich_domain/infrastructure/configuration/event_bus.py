import injector

from modules.another_rich_domain.core.application.bounded_context_translators import (
    RichDomainModelCreatedIntegrationEventTranslator,
)
from modules.another_rich_domain.core.application.event_handlers import UpdateThisResource
from modules.another_rich_domain.core.domain.events import SomeResourceCreated
from modules.another_rich_domain.core.types import Module1

from commons.event_bus.application.event_bus import EventBus
from commons.messagebox.application.generic_event_handlers import GenericStoreIntegrationEventInInbox
from commons.messagebox.application.message_handlers import IntegrationEventMessageHandler
from commons.messagebox.application.process_messagebox_handlers import (
    ProcessInboxHandler,
)
from commons.messagebox.infrastructure.messagebox import MessageTopic


class EventsSubscriptionsConfigurator:
    @injector.inject
    def __init__(
        self,
        container: injector.Injector,
        event_bus: EventBus,
        process_inbox_handler: ProcessInboxHandler,
        module_1: Module1,
    ) -> None:
        self._container = container
        self._event_bus = event_bus
        self._process_inbox_handler = process_inbox_handler
        self._module_1 = module_1

    @injector.inject
    def configure_subscriptions(
        self,
        event_bus: EventBus,
    ) -> None:
        for event_cls, handler_cls in [
            (SomeResourceCreated, UpdateThisResource),
        ]:
            event_bus.subscribe(event_cls, self._container.get(handler_cls))

        event_bus.subscribe(
            self._module_1.RichDomainModelCreatedIntegrationEvent,
            self._container.get(GenericStoreIntegrationEventInInbox),
        )

        self._process_inbox_handler.add_handler(
            MessageTopic(self._module_1.RichDomainModelCreatedIntegrationEvent.event_name()),
            IntegrationEventMessageHandler(
                RichDomainModelCreatedIntegrationEventTranslator(),
                self._event_bus,
            ),
        )
