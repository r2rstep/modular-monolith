import injector

from commons.container.infrastructure import scopes
from commons.event_bus.application.event_bus import EventBus


class GlobalContainer(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=scopes.context_scope)


global_container = injector.Injector(GlobalContainer())
