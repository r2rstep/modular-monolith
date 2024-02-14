from modules.another_rich_domain.core.application.messagebox import ProcessInbox

from commons.message_bus.message_bus import MessageBus
from modules.another_rich_domain.infrastructure.container import get_container


class Module:
    message_bus = get_container().get(MessageBus)
    ProcessInbox = ProcessInbox


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module"]
