import functools

import injector

from modules.another_rich_domain.core.application.messagebox import ProcessInbox, ProcessOutbox

from commons.container.infrastructure.global_container import get_global_container
from commons.message_bus.message_bus import (
    MessageBus,
)
from commons.messagebox.application.process_messagebox_commands import (
    ProcessInbox as ProcessInboxBase,
    ProcessOutbox as ProcessOutboxBase,
)
from commons.messagebox.infrastructure.messagebox import Inbox
from modules.another_rich_domain.infrastructure.configuration.inbox import init_inbox


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(MessageBus, to=MessageBus, scope=injector.singleton)

    @injector.provider
    @injector.singleton
    @injector.provider
    def inbox_provider(self) -> Inbox:
        return init_inbox()

    @injector.singleton
    @injector.provider
    def process_inbox_command_provider(self) -> type[ProcessInboxBase]:
        return ProcessInbox

    @injector.singleton
    @injector.provider
    def process_outbox_command_provider(self) -> type[ProcessOutboxBase]:
        return ProcessOutbox


@functools.lru_cache
def get_container() -> injector.Injector:
    container = get_global_container().create_child_injector(Container())
    container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
    return container
