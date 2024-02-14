import injector

from modules.another_rich_domain.core.application.messagebox import ProcessInbox

from commons.message_bus.message_bus import CommandToHandlerMapping
from commons.messagebox.application.process_messagebox_handlers import ProcessInboxHandler


@injector.inject
def configure_commands_mapping(commands_mapping: CommandToHandlerMapping) -> None:
    commands_mapping[ProcessInbox] = ProcessInboxHandler
