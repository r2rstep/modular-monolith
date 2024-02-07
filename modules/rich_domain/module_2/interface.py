from modules.rich_domain.module_2.core.application.messagebox import ProcessInbox, ProcessOutbox
from modules.rich_domain.module_2.core.application.query import GetSomething

from commons.message_bus.message_bus import MessageBus
from modules.rich_domain.module_2.infrastructure.container import get_container


# @dataclass(frozen=True)
class Module:
    message_bus = get_container().get(MessageBus)
    GetSomething = GetSomething
    ProcessInbox = ProcessInbox
    ProcessOutbox = ProcessOutbox


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module"]
