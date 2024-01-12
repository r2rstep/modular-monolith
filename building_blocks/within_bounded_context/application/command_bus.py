import injector

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from commons.types import PK, NoneOr

CommandToHandlerMapping = dict[type[Command], type[CommandHandler[Command]]]


class CommandBus:
    @injector.inject
    def __init__(self, commands_mapping: CommandToHandlerMapping, container: injector.Injector) -> None:
        self._commands_mapping = commands_mapping
        self._container = container

    async def execute(self, command: Command) -> NoneOr[PK]:
        # TODO @R2RStep: implement proper outbox handling
        # https://github.com/r2rstep/modular-monolith/issues/19
        handler_cls = self._commands_mapping[type(command)]
        result = await self._container.get(handler_cls).handle(command)
        await self._container.get(self._commands_mapping["ProcessOutbox"]).handle(None)  # type: ignore[index, arg-type]
        return result

    async def execute_internal(self, command: Command) -> NoneOr[PK]:
        """
        Executes commands when all the context has already been set up
        """
        handler_cls = self._commands_mapping[type(command)]
        return await self._container.get(handler_cls).handle(command)
