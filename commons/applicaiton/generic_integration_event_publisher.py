from typing import cast

import injector

from building_blocks.application.event_handlers import NotificationEventHandler
from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent, DomainEventType, is_public_event
from commons.event_bus.application.event_bus import EventBus


class GenericIntegrationEventPublisher(NotificationEventHandler[DomainEventType]):
    _integration_event_cls: type[IntegrationEvent]

    @injector.inject
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    async def handle(self, event: NotificationEvent[DomainEventType]) -> None:
        await self._event_bus.publish(
            IntegrationEvent.from_notification_event(notification_event=cast(NotificationEvent[DomainEvent], event))
        )


def build_generic_publish_integration_event_handler(
    integration_event_cls: type[IntegrationEvent], originating_domain_event_cls: type[DomainEventType]
) -> type[GenericIntegrationEventPublisher[DomainEventType]]:
    assert is_public_event(originating_domain_event_cls)  # noqa: S101

    return cast(
        type[GenericIntegrationEventPublisher[DomainEventType]],
        type(
            f"Publish{integration_event_cls.__name__}",
            (GenericIntegrationEventPublisher,),
            {"_integration_event_cls": integration_event_cls},
        ),
    )
