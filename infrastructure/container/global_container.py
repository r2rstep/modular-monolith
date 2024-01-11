import injector

from infrastructure.container import scopes
from infrastructure.event_bus import EventBus


class GlobalContainer(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=scopes.context_scope)


global_container = injector.Injector(GlobalContainer())
