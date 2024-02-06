from dataclasses import dataclass, field

from modules.crud.core.application.commands.messagebox import ProcessInbox
from modules.crud.core.application.queries.get import GetCrudData

from commons.message_bus.message_bus import MessageBus
from modules.crud.infrastructure.container import get_container


@dataclass
class Module:
    message_bus: MessageBus = field(default_factory=lambda: get_container().get(MessageBus), init=False)
    GetCrudData = GetCrudData
    ProcessInbox = ProcessInbox


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module"]
