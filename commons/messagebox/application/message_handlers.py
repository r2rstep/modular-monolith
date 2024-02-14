from abc import ABC, abstractmethod

from building_blocks.application.bounded_context_translator import BoundedContextTranslator
from building_blocks.application.command import Command
from building_blocks.application.notification_event import NotificationEvent
from commons.event_bus.application.event_bus import EventBus
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.infrastructure.messagebox import MessagePayload


class MessageHandler(ABC):
    @abstractmethod
    async def handle(self, message_payload: MessagePayload) -> None:
        ...


class CommandMessageHandler(MessageHandler):
    def __init__(self, command_cls: type[Command], message_bus: MessageBus) -> None:
        self._message_bus = message_bus
        self._command_cls = command_cls

    async def handle(self, message_payload: MessagePayload) -> None:
        command = self._command_cls(**message_payload)
        await self._message_bus.execute_internal(command)


class NotificationEventMessageHandler(MessageHandler):
    def __init__(self, notification_event_cls: type[NotificationEvent], event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._event_cls = notification_event_cls

    async def handle(self, message_payload: MessagePayload) -> None:
        notification_serialized = message_payload
        notification = self._event_cls(**notification_serialized)
        await self._event_bus.publish(notification)


class IntegrationEventMessageHandler(MessageHandler):
    def __init__(
        self,
        translator: BoundedContextTranslator,
        event_bus: EventBus,
    ) -> None:
        self._event_bus = event_bus
        self._translator = translator

    async def handle(self, message_payload: MessagePayload) -> None:
        event = self._translator.translate(message_payload)
        await self._event_bus.publish(event)
