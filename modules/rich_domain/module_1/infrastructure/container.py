import injector

from building_blocks.within_bounded_context.infrastructure.command_bus import CommandBus, CommandToHandlerMapping
from infrastructure.container.global_container import GlobalContainer


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        commands_mapping = {}
        binder.multibind(
            CommandToHandlerMapping,
            to=commands_mapping,
            scope=injector.singleton,
        )
        binder.bind(
            CommandBus,
            to=CommandBus,
            scope=injector.singleton,
        )


container = injector.Injector([Container(), GlobalContainer()])
container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
