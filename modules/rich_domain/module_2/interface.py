import injector

from modules.rich_domain.module_2.core.application.query import GetSomething

from building_blocks.within_bounded_context.application.command_bus import MessageBus
from building_blocks.within_bounded_context.module.module import ModuleInterface
from modules.rich_domain.module_2.infrastructure.container import container


class Module(ModuleInterface):
    @injector.inject
    def __init__(self, command_bus: MessageBus):
        self.command_bus = command_bus


def get_module() -> Module:
    return container.get(Module)


__all__ = ["get_module", "GetSomething"]
