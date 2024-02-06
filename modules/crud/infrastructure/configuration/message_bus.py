from typing import cast

import injector

from modules.crud.core.application.commands.messagebox import ProcessInbox
from modules.crud.core.application.queries.get import GetCrudData, GetCrudDataHandler

from building_blocks.within_bounded_context.application.query import Query, QueryHandler
from commons.message_bus.message_bus import (
    CommandToHandlerMapping,
    QueryToHandlerMapping,
)
from commons.messagebox.application.process_messagebox_handlers import (
    ProcessInboxCommandsHandler,
)


@injector.inject
def configure_commands_mapping(commands_mapping: CommandToHandlerMapping) -> None:
    commands_mapping[ProcessInbox] = ProcessInboxCommandsHandler


@injector.inject
def configure_queries_mapping(queries_mapping: QueryToHandlerMapping) -> None:
    for query, handler_cls in [
        (GetCrudData, GetCrudDataHandler),
    ]:
        queries_mapping[query] = cast(type[QueryHandler[Query]], handler_cls)
