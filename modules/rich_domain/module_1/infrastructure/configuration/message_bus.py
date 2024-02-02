from typing import cast

import injector

from modules.rich_domain.module_1.core.application.commands.rich_domain_model import (
    CreateRichDomainModel,
    CreateRichDomainModelHandler,
)
from modules.rich_domain.module_1.core.application.queries.get_a import GetA, GetAHandler

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
        (CreateRichDomainModel, CreateRichDomainModelHandler),
    ]:
        commands_mapping[command] = cast(type[CommandHandler[Command]], handler_cls)


@injector.inject
def configure_queries_mapping(queries_mapping: QueryToHandlerMapping) -> None:
    for query, handler_cls in [
        (GetA, GetAHandler),
    ]:
        queries_mapping[query] = cast(type[QueryHandler[Query]], handler_cls)
