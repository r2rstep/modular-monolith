from typing import cast

import injector

from building_blocks.application.command import Command
from building_blocks.application.event_handlers import (
    DomainEventHandler,
    IntegrationEventHandler,
    NotificationEventHandler,
)
from building_blocks.application.integration_event import IntegrationEventType
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEventType
from commons.messagebox.infrastructure.messagebox import Inbox, MessageTopic, Outbox
from commons.utils import get_annotations


class GenericStoreNotificationEventInOutbox(DomainEventHandler[DomainEventType]):
    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        self._outbox = outbox

    async def handle(self, event: DomainEventType) -> None:
        await self._outbox.add(MessageTopic(event.event_name()), dict(NotificationEvent(domain_event=event)))


class GenericStoreIntegrationEventInInbox(IntegrationEventHandler[IntegrationEventType]):
    @injector.inject
    def __init__(self, inbox: Inbox) -> None:
        self._inbox = inbox

    async def handle(self, event: IntegrationEventType) -> None:
        await self._inbox.add(MessageTopic(event.event_name()), dict(event))


class GenericStoreCommandBasedOnNotificationEventInInbox(NotificationEventHandler[DomainEventType]):
    _command_cls: type[Command]

    def __init__(self, inbox: injector.Inject[Inbox]) -> None:
        self._inbox = inbox

    async def handle(self, notification: NotificationEvent[DomainEventType]) -> None:
        domain_event = notification.domain_event
        event_annotations = get_annotations(domain_event.__class__)
        command_annotations = get_annotations(self._command_cls)

        if not set(command_annotations.keys()).issubset(set(event_annotations.keys())):
            exception_message = (
                "Command attributes are not a subset of event attributes."
                f" Command: {self._command_cls}, event: {domain_event.__class__}"
            )
            raise ValueError(exception_message)

        if not all(
            command_annotations[cmd_attribute] == event_annotations[cmd_attribute]
            for cmd_attribute in command_annotations
        ):
            exception_message = (
                f"Command and event attributes have different annotations."
                f" Command: {self._command_cls}, event: {domain_event.__class__}"
            )
            raise ValueError(exception_message)

        command_payload = {key: getattr(domain_event, key) for key in command_annotations}
        await self._inbox.add_idempotent(
            MessageTopic(self._command_cls.__name__), command_payload, notification.idempotency_id
        )


def build_store_command_in_inbox_handler(
    command_cls: type[Command], _: type[DomainEventType]
) -> type[GenericStoreCommandBasedOnNotificationEventInInbox[DomainEventType]]:
    return cast(
        type[GenericStoreCommandBasedOnNotificationEventInInbox[DomainEventType]],
        type(
            f"Store{command_cls.__name__}InInbox",
            (GenericStoreCommandBasedOnNotificationEventInInbox,),
            {"_command_cls": command_cls},
        ),
    )
