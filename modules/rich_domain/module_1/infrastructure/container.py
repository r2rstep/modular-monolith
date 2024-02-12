import functools

import injector

from modules.rich_domain.module_1.core.application.commands.messagebox import ProcessInbox, ProcessOutbox

from commons.container.infrastructure.global_container import get_global_container
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.application.process_messagebox_commands import (
    ProcessInbox as ProcessInboxBase,
    ProcessOutbox as ProcessOutboxBase,
)
from commons.messagebox.infrastructure.messagebox import Inbox, Outbox
from modules.rich_domain.module_1.infrastructure.configuration.inbox import init_inbox
from modules.rich_domain.module_1.infrastructure.configuration.outbox import init_outbox


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(MessageBus, to=MessageBus, scope=injector.singleton)

    @injector.singleton
    @injector.provider
    def outbox_provider(self) -> Outbox:
        return init_outbox()

    @injector.singleton
    @injector.provider
    def process_outbox_command_provider(self) -> type[ProcessOutboxBase]:
        return ProcessOutbox

    @injector.singleton
    @injector.provider
    def inbox_provider(self) -> Inbox:
        return init_inbox()

    @injector.singleton
    @injector.provider
    def process_inbox_command_provider(self) -> type[ProcessInboxBase]:
        return ProcessInbox


@functools.lru_cache
def get_container() -> injector.Injector:
    container = get_global_container().create_child_injector(Container())
    container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
    return container
