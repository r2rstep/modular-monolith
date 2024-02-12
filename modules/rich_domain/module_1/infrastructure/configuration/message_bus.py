from typing import cast

import injector

from modules.rich_domain.module_1.core.application.commands.messagebox import ProcessInbox, ProcessOutbox
from modules.rich_domain.module_1.core.application.commands.rich_domain_model import (
    CreateRichDomainModel,
    CreateRichDomainModelHandler,
)
from modules.rich_domain.module_1.core.application.queries.get_a import GetA, GetAHandler

from building_blocks.application.command import Command, CommandHandler
from building_blocks.application.query import Query, QueryHandler
from commons.message_bus.message_bus import (
    CommandToHandlerMapping,
    QueryToHandlerMapping,
)
from commons.messagebox.application.process_messagebox_handlers import (
    ProcessInboxHandler,
    ProcessOutboxHandler,
)


@injector.inject
def configure_commands_mapping(commands_mapping: CommandToHandlerMapping) -> None:
    commands_mapping[ProcessOutbox] = ProcessOutboxHandler
    commands_mapping[ProcessInbox] = ProcessInboxHandler
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
