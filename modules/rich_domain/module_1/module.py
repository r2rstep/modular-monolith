import injector

from building_blocks.within_bounded_context.infrastructure.command_bus import CommandBus
from building_blocks.within_bounded_context.module.module import ModuleInterface
from modules.rich_domain.module_1.infrastructure.container import container


class Module(ModuleInterface):
    @injector.inject
    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus


module_1 = Module(container.get(CommandBus))
