from modules.crud.core.application.commands.messagebox import ProcessInbox
from modules.crud.core.application.queries.get import GetCrudData

from commons.message_bus.message_bus import MessageBus
from modules.crud.infrastructure.container import get_container


# @dataclass(frozen=True)
class Module:
    message_bus = get_container().get(MessageBus)
    GetCrudData = GetCrudData
    ProcessInbox = ProcessInbox


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module"]
