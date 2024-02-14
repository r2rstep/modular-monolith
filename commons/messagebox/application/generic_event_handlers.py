from typing import cast

import injector

from building_blocks.application.command import Command
from building_blocks.application.event_handlers import (
    DomainEventHandler,
    IntegrationEventHandler,
    NotificationEventHandler,
)
from building_blocks.application.integration_event import IntegrationEventType
from building_blocks.application.notification_event import NotificationEvent, NotificationEventType
from building_blocks.domain.event import DomainEventType
from commons.messagebox.infrastructure.messagebox import Inbox, MessageTopic, Outbox
from commons.utils import get_annotations


class GenericStoreNotificationEventInOutbox(DomainEventHandler[DomainEventType]):
    _notification_event_cls: type[NotificationEvent]

    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        self._outbox = outbox

    async def handle(self, domain_event: DomainEventType) -> None:
        notification = self._notification_event_cls.from_domain_event(domain_event)
        await self._outbox.add(MessageTopic(notification.event_name()), dict(notification))


def build_store_notification_in_outbox_handler(
    notification_cls: type[NotificationEvent], _: type[DomainEventType]
) -> type[GenericStoreNotificationEventInOutbox[DomainEventType]]:
    return cast(
        type[GenericStoreNotificationEventInOutbox[DomainEventType]],
        type(
            f"Store{notification_cls.__name__}InOutbox",
            (GenericStoreNotificationEventInOutbox,),
            {"_notification_event_cls": notification_cls},
        ),
    )


class GenericStoreIntegrationEventInInbox(IntegrationEventHandler[IntegrationEventType]):
    @injector.inject
    def __init__(self, inbox: Inbox) -> None:
        self._inbox = inbox

    async def handle(self, event: IntegrationEventType) -> None:
        await self._inbox.add(MessageTopic(event.event_name()), dict(event))


class GenericStoreCommandBasedOnNotificationEventInInbox(NotificationEventHandler[NotificationEventType]):
    _command_cls: type[Command]

    def __init__(self, inbox: injector.Inject[Inbox]) -> None:
        self._inbox = inbox

    async def handle(self, notification: NotificationEventType) -> None:
        event_annotations = get_annotations(notification.__class__)
        command_annotations = get_annotations(self._command_cls)

        if not set(command_annotations.keys()).issubset(set(event_annotations.keys())):
            exception_message = (
                "Command attributes are not a subset of event attributes."
                f" Command: {self._command_cls}, event: {notification.__class__}"
            )
            raise ValueError(exception_message)

        if not all(
            command_annotations[cmd_attribute] == event_annotations[cmd_attribute]
            for cmd_attribute in command_annotations
        ):
            exception_message = (
                f"Command and event attributes have different annotations."
                f" Command: {self._command_cls}, event: {notification.__class__}"
            )
            raise ValueError(exception_message)

        command_payload = {key: getattr(notification, key) for key in command_annotations}
        await self._inbox.add_idempotent(
            MessageTopic(self._command_cls.command_name()), command_payload, notification.idempotency_id
        )


def build_store_command_in_inbox_handler(
    command_cls: type[Command], _: type[NotificationEventType]
) -> type[GenericStoreCommandBasedOnNotificationEventInInbox[NotificationEventType]]:
    return cast(
        type[GenericStoreCommandBasedOnNotificationEventInInbox[NotificationEventType]],
        type(
            f"Store{command_cls.__name__}InInbox",
            (GenericStoreCommandBasedOnNotificationEventInInbox,),
            {"_command_cls": command_cls},
        ),
    )
