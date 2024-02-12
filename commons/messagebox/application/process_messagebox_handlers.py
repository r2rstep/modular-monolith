import injector

from building_blocks.application.command import Command, CommandHandler
from commons.messagebox.application.message_handlers import MessageHandler
from commons.messagebox.infrastructure.messagebox import (
    Inbox,
    Messagebox,
    MessageTopic,
    Outbox,
)


class ProcessMessageboxHandler(CommandHandler[Command]):
    @injector.inject
    def __init__(self, messagebox: Messagebox) -> None:
        self._messagebox = messagebox
        self._handlers: dict[MessageTopic, MessageHandler] = {}

    def add_handler(self, topic: MessageTopic, handler: MessageHandler) -> None:
        self._handlers.update({topic: handler})

    async def handle(self, _: Command) -> None:
        failed_messages = []
        while (message := await self._messagebox.get_next()) is not None:
            try:
                await self._handlers[message.topic].handle(message.payload)
            except KeyError:  # noqa: PERF203
                # TODO @R2RStep: add logging
                # https://github.com/r2rstep/modular-monolith/issues/18
                continue
            except Exception:  # noqa: BLE001
                failed_messages.append(message)

        for message in failed_messages:
            await self._messagebox.add(message.topic, message.payload)


class ProcessOutboxHandler(ProcessMessageboxHandler):
    @injector.inject
    def __init__(self, outbox: Outbox) -> None:
        super().__init__(outbox)


class ProcessInboxHandler(ProcessMessageboxHandler):
    @injector.inject
    def __init__(self, inbox: Inbox) -> None:
        super().__init__(inbox)
