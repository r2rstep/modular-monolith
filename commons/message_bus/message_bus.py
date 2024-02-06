from typing import Optional

import injector

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from building_blocks.within_bounded_context.application.query import Query, QueryHandler
from commons.messagebox.application.process_messagebox_commands import ProcessOutbox
from commons.types import PK, NoneOr


class CommandToHandlerMapping(dict[type[Command], type[CommandHandler[Command]]]):
    ...


class QueryToHandlerMapping(dict[type[Query], type[QueryHandler[Query]]]):
    ...


class MessageBus:
    @injector.inject
    def __init__(
        self,
        commands_mapping: CommandToHandlerMapping,
        queries_mapping: QueryToHandlerMapping,
        container: injector.Injector,
        # TODO @R2RStep: implement proper outbox handling
        # https://github.com/r2rstep/modular-monolith/issues/19
        process_outbox_command: Optional[type[ProcessOutbox]] = None,
    ) -> None:
        self._commands_mapping = commands_mapping
        self._queries_mapping = queries_mapping
        self._container = container
        self._process_outbox_command = process_outbox_command

    async def execute(self, command: Command) -> NoneOr[PK]:
        handler_cls = self._commands_mapping[type(command)]
        result = await self._container.get(handler_cls).handle(command)
        if self._process_outbox_command:
            await self._container.get(self._commands_mapping[self._process_outbox_command]).handle(
                self._process_outbox_command()
            )
        return result

    async def execute_internal(self, command: Command) -> NoneOr[PK]:
        """
        Executes commands when all the context has already been set up
        """
        handler_cls = self._commands_mapping[type(command)]
        return await self._container.get(handler_cls).handle(command)

    # No return type annotation as caller would probably cast the result either way
    # To reconsider if a caller would somehow need to use dataclass methods on the result (the result is a dataclass)
    async def query(self, query: Query):  # type: ignore[no-untyped-def] # noqa: ANN201
        """
        Can also be used to execute internal queries. This assumes that "read committed" is ensured without the need of
         opening a transaction.
        """
        handler_cls = self._queries_mapping[type(query)]
        return await self._container.get(handler_cls).handle(query)
