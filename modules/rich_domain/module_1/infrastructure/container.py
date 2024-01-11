import injector

from building_blocks.within_bounded_context.application.command_bus import CommandBus, CommandToHandlerMapping
from infrastructure.container.global_container import GlobalContainer
from infrastructure.messagebox import Inbox, Outbox
from modules.rich_domain.module_2.infrastructure.configuration.inbox import init_inbox
from modules.rich_domain.module_2.infrastructure.configuration.outbox import init_outbox


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

    @injector.singleton
    @injector.provider
    def inbox_provider(self) -> Inbox:
        return init_inbox()


container = injector.Injector([Container(), GlobalContainer()])
container.binder.bind(injector.Injector, to=container, scope=injector.singleton)
