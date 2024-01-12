from typing import cast

import injector

from modules.rich_domain.module_2.core.application.module_1_events_handlers import CreateSomething, DoSomething

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from building_blocks.within_bounded_context.application.command_bus import CommandToHandlerMapping
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
