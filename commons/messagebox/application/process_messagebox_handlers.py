import injector

from building_blocks.application.command import Command, CommandHandler
from commons.messagebox.application.message_handlers import MessageHandler
from commons.messagebox.infrastructure.messagebox import (
    Inbox,
    Messagebox,
    MessageTopic,
    Outbox,
)

MessageHandlers = dict[MessageTopic, MessageHandler]


class ProcessMessageboxHandler(CommandHandler[Command]):
    @injector.inject
    def __init__(self, messagebox: Messagebox, handlers: MessageHandlers) -> None:
        self._messagebox = messagebox
        self._handlers = handlers

    def add_handler(self, topic: MessageTopic, handler: MessageHandler) -> None:
        self._handlers.update({topic: handler})

    async def handle(self, _: Command) -> None:
        with self._messagebox.open():
            while message := await self._messagebox.get_next_pending():
                try:
                    await self._handlers[message["topic"]].handle(message["payload"])
                except KeyError:  # noqa: PERF203
                    # TODO @R2RStep: add logging
                    # https://github.com/r2rstep/modular-monolith/issues/18
                    continue


class ProcessOutboxHandler(ProcessMessageboxHandler):
    @injector.inject
    def __init__(self, outbox: Outbox, handlers: MessageHandlers) -> None:
        super().__init__(outbox, handlers)


class ProcessInboxHandler(ProcessMessageboxHandler):
    @injector.inject
    def __init__(self, inbox: Inbox, handlers: MessageHandlers) -> None:
        super().__init__(inbox, handlers)
