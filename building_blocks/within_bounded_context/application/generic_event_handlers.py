from typing import cast

import injector

from building_blocks.within_bounded_context.application.command import Command
from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent
from infrastructure.messagebox import Inbox, MessageName, Outbox
from infrastructure.utils import get_annotations


class GenericStorePublicEventInOutbox(DomainEventHandler[DomainEvent]):
    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        self._outbox = outbox

    async def handle(self, event: DomainEvent) -> None:
        if event.is_public:
            await self._outbox.add(MessageName(event.name), dict(event))


class GenericStoreCommandBasedOnEventInInbox(DomainEventHandler[DomainEvent]):
    _command_cls: type[Command]

    def __init__(self, inbox: injector.Inject[Inbox]) -> None:
        self._inbox = inbox

    async def handle(self, event: DomainEvent) -> None:
        event_annotations = get_annotations(event.__class__)
        command_annotations = get_annotations(self._command_cls)

        if not set(command_annotations.keys()).issubset(set(event_annotations.keys())):
            exception_message = (
                "Command attributes are not a subset of event attributes."
                f" Command: {self._command_cls}, event: {event.__class__}"
            )
            raise ValueError(exception_message)

        if not all(
            command_annotations[cmd_attribute] == event_annotations[cmd_attribute]
            for cmd_attribute in command_annotations
        ):
            exception_message = (
                f"Command and event attributes have different annotations."
                f" Command: {self._command_cls}, event: {event.__class__}"
            )
            raise ValueError(exception_message)

        command_payload = {key: getattr(event, key) for key in command_annotations}
        await self._inbox.add_idempotent(MessageName(self._command_cls.__name__), command_payload, event.idempotence_id)


def build_store_command_in_inbox_handler(command_cls: type[Command]) -> type[GenericStoreCommandBasedOnEventInInbox]:
    return cast(
        type[GenericStoreCommandBasedOnEventInInbox],
        type(
            f"Store{command_cls.__name__}InInbox",
            (GenericStoreCommandBasedOnEventInInbox,),
            {"_command_cls": command_cls},
        ),
    )
