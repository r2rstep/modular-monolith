import injector

from building_blocks.types import PK
from building_blocks.within_bounded_context.application.command import Command, CommandHandler

CommandToHandlerMapping = dict[type[Command], type[CommandHandler]]


class CommandBus:
    @injector.inject
    def __init__(self, commands_mapping: CommandToHandlerMapping, container: injector.Injector) -> None:
        self._commands_mapping = commands_mapping
        self._container = container

    async def execute(self, command: Command) -> PK:
        handler_cls = self._commands_mapping.get(type(command))
        return await self._container.get(handler_cls).handle(command)
