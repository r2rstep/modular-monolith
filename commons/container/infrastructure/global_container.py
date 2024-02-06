import functools

import injector

from commons.container.infrastructure import scopes
from commons.event_bus.application.event_bus import EventBus
from commons.message_bus.message_bus import (
    CommandToHandlerMapping,
    QueryToHandlerMapping,
)


class GlobalContainer(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=scopes.context_scope)

    @injector.singleton
    @injector.provider
    def get_commands_mapping(self) -> CommandToHandlerMapping:
        return CommandToHandlerMapping()

    @injector.singleton
    @injector.provider
    def get_queries_mapping(self) -> QueryToHandlerMapping:
        return QueryToHandlerMapping()


@functools.lru_cache
def get_global_container() -> injector.Injector:
    return injector.Injector(GlobalContainer(), auto_bind=False)
