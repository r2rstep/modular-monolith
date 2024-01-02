import injector

from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus
from infrastructure.container import scopes


class GlobalContainer(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=scopes.context_scope)


global_container = injector.Injector(GlobalContainer())
