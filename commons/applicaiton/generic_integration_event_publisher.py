from typing import cast

import injector

from building_blocks.application.event_handlers import NotificationEventHandler
from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent, NotificationEventType
from commons.event_bus.application.event_bus import EventBus


class GenericIntegrationEventPublisher(NotificationEventHandler[NotificationEventType]):
    _integration_event_cls: type[IntegrationEvent]

    @injector.inject
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    async def handle(self, event: NotificationEvent) -> None:
        await self._event_bus.publish(self._integration_event_cls.from_notification_event(notification_event=event))


def build_generic_publish_integration_event_handler(
    integration_event_cls: type[IntegrationEvent], _: type[NotificationEventType]
) -> type[GenericIntegrationEventPublisher[NotificationEventType]]:
    return cast(
        type[GenericIntegrationEventPublisher[NotificationEventType]],
        type(
            f"Publish{integration_event_cls.__name__}",
            (GenericIntegrationEventPublisher,),
            {"_integration_event_cls": integration_event_cls},
        ),
    )
