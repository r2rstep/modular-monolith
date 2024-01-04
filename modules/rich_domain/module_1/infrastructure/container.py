import injector

from building_blocks.within_bounded_context.infrastructure.command_bus import CommandBus, CommandToHandlerMapping
from building_blocks.within_bounded_context.infrastructure.messagebox import Outbox
from infrastructure.container.global_container import GlobalContainer
from modules.rich_domain.module_1.infrastructure.configuration.outbox import init_outbox


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

    @injector.singleton
    @injector.provider
    def outbox_provider(self) -> Outbox:
        return init_outbox()


container = injector.Injector([Container(), GlobalContainer()])
container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
