import functools

import injector

from modules.rich_domain.module_2.core.application.messagebox import ProcessInbox, ProcessOutbox

from commons.container.infrastructure.global_container import get_global_container
from commons.message_bus.message_bus import (
    MessageBus,
)
from commons.messagebox.application.process_messagebox_commands import (
    ProcessInbox as ProcessInboxBase,
    ProcessOutbox as ProcessOutboxBase,
)
from commons.messagebox.infrastructure.messagebox import Inbox, Outbox
from commons.messagebox.types import CommandsList, PublicDomainEventsClsList
from modules.rich_domain.module_2.infrastructure.configuration.inbox import init_inbox
from modules.rich_domain.module_2.infrastructure.configuration.outbox import init_outbox
from modules.rich_domain.ports.adapters.api_clients import MessageBusCrudApiClient
from modules.rich_domain.ports.api_clients import CrudApiClient


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(MessageBus, to=MessageBus, scope=injector.singleton)
        binder.multibind(PublicDomainEventsClsList, to=[], scope=injector.singleton)
        binder.multibind(CommandsList, to=[], scope=injector.singleton)
        binder.bind(CrudApiClient, to=MessageBusCrudApiClient)  # type: ignore[type-abstract]

    @injector.singleton
    @injector.provider
    def outbox_provider(self) -> Outbox:
        return init_outbox()

    @injector.singleton
    @injector.provider
    def process_outbox_command_provider(self) -> type[ProcessOutboxBase]:
        return ProcessOutbox

    @injector.provider
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
