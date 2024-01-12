import injector

from building_blocks.within_bounded_context.application.command_bus import CommandBus, CommandToHandlerMapping
from commons.container.infrastructure.global_container import GlobalContainer
from commons.messagebox.infrastructure.messagebox import Inbox, Outbox
from commons.messagebox.types import CommandsList, PublicDomainEventsClsList
from modules.rich_domain.module_2.infrastructure.configuration.inbox import init_inbox
from modules.rich_domain.module_2.infrastructure.configuration.outbox import init_outbox


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.multibind(CommandToHandlerMapping, to={}, scope=injector.singleton)
        binder.bind(CommandBus, to=CommandBus, scope=injector.singleton)
        binder.multibind(PublicDomainEventsClsList, to=[], scope=injector.singleton)
        binder.multibind(CommandsList, to=[], scope=injector.singleton)

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
