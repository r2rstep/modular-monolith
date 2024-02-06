from abc import abstractmethod
from typing import Generic, TypeVar

import injector

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from building_blocks.within_bounded_context.application.notification_event import NotificationEvent
from building_blocks.within_bounded_context.domain.events import DomainEvent
from commons.event_bus.application.event_bus import EventBus
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.infrastructure.messagebox import Inbox, Messagebox, MessageDTO, Outbox
from commons.messagebox.types import CommandsList, PublicDomainEventsClsList

PayloadType = TypeVar("PayloadType", DomainEvent, Command)


class ProcessMessageboxHandler(CommandHandler[Command], Generic[PayloadType]):
    @injector.inject
    def __init__(self, messagebox: Messagebox, payload_cls_list: list[type[PayloadType]]) -> None:
        self._messagebox = messagebox
        self._payload_cls_mapping: dict[str, type[PayloadType]] = {cls.__name__: cls for cls in payload_cls_list}

    async def handle(self, _: Command) -> None:
        failed_messages = []
        while (message := await self._messagebox.get_next()) is not None:
            try:
                if message.name not in self._payload_cls_mapping:
                    # TODO @R2RStep: add logging
                    # https://github.com/r2rstep/modular-monolith/issues/18
                    continue
                payload_cls = next(
                    event_cls
                    for event_name, event_cls in self._payload_cls_mapping.items()
                    if event_name == message.name
                )
                await self._process_message(payload_cls, message)
            except Exception:  # noqa: BLE001
                failed_messages.append(message)

        for message in failed_messages:
            await self._messagebox.add(message.name, message.payload)

    @abstractmethod
    async def _process_message(self, event_cls: type[PayloadType], message: MessageDTO) -> None:
        ...


class ProcessOutboxDomainEventsHandler(ProcessMessageboxHandler[DomainEvent]):
    @injector.inject
    def __init__(self, outbox: Outbox, event_bus: EventBus, domain_events_cls_list: PublicDomainEventsClsList) -> None:
        self._event_bus = event_bus
        super().__init__(outbox, domain_events_cls_list)

    async def _process_message(self, event_cls: type[DomainEvent], message: MessageDTO) -> None:
        notification_serialized = message.payload
        notification: NotificationEvent[DomainEvent] = NotificationEvent(
            domain_event=event_cls(**notification_serialized["domain_event"]),
            idempotency_id=notification_serialized["idempotency_id"],
        )
        await self._event_bus.publish(notification)


class ProcessInboxCommandsHandler(ProcessMessageboxHandler[Command]):
    @injector.inject
    def __init__(self, inbox: Inbox, message_bus: MessageBus, commands_cls_list: CommandsList) -> None:
        self._command_bus = message_bus
        super().__init__(inbox, commands_cls_list)

    async def _process_message(self, command_cls: type[Command], message: MessageDTO) -> None:
        command = command_cls(**message.payload)
        await self._command_bus.execute_internal(command)
