from typing import cast

import injector

from modules.rich_domain.module_2.core.application.module_1_events_handlers import CreateSomething, DoSomething
from modules.rich_domain.module_2.core.application.query import GetSomething, GetSomethingHandler

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from building_blocks.within_bounded_context.application.message_bus import (
    CommandToHandlerMapping,
    QueryToHandlerMapping,
)
from building_blocks.within_bounded_context.application.query import Query, QueryHandler
from commons.messagebox.application.process_messagebox import (
    ProcessInbox,
    ProcessInboxCommandsHandler,
    ProcessOutboxDomainEventsHandler,
)


@injector.inject
def configure_commands_mapping(commands_mapping: CommandToHandlerMapping) -> None:
    commands_mapping["ProcessOutbox"] = ProcessOutboxDomainEventsHandler  # type: ignore[index]
    commands_mapping[ProcessInbox] = ProcessInboxCommandsHandler
    for command, handler_cls in [
        (DoSomething, CreateSomething),
    ]:
        commands_mapping[command] = cast(type[CommandHandler[Command]], handler_cls)


@injector.inject
def configure_queries_mapping(queries_mapping: QueryToHandlerMapping) -> None:
    for query, handler_cls in [
        (GetSomething, GetSomethingHandler),
    ]:
        queries_mapping[query] = cast(type[QueryHandler[Query]], handler_cls)
