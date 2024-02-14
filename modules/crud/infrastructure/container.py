import functools

import injector

from modules.crud.core.application.commands.messagebox import ProcessInbox

from commons.container.infrastructure.global_container import get_global_container
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.application.process_messagebox_commands import (
    ProcessInbox as ProcessInboxBase,
    ProcessOutbox as ProcessOutboxBase,
)
from commons.messagebox.application.process_messagebox_handlers import MessageHandlers
from commons.messagebox.infrastructure.messagebox import Inbox
from modules.crud.infrastructure.configuration.inbox import init_inbox


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(MessageBus, to=MessageBus, scope=injector.singleton)
        binder.multibind(MessageHandlers, to={}, scope=injector.singleton)

    @injector.singleton
    @injector.provider
    def inbox_provider(self) -> Inbox:
        return init_inbox()

    @injector.singleton
    @injector.provider
    def process_inbox_command(self) -> type[ProcessInboxBase]:
        return ProcessInbox

    @injector.singleton
    @injector.provider
    def process_outbox_command(self) -> type[ProcessOutboxBase]:
        return None  # type: ignore[return-value]


@functools.lru_cache
def get_container() -> injector.Injector:
    container = get_global_container().create_child_injector(Container())
    container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
    return container
