from dataclasses import dataclass, field

from modules.rich_domain.module_1.core.application.commands.messagebox import ProcessInbox, ProcessOutbox
from modules.rich_domain.module_1.core.application.commands.rich_domain_model import CreateRichDomainModel
from modules.rich_domain.module_1.core.application.queries.get_a import GetA
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from commons.message_bus.message_bus import MessageBus
from modules.rich_domain.module_1.infrastructure.container import get_container


@dataclass
class Module:
    message_bus: MessageBus = field(default_factory=lambda: get_container().get(MessageBus), init=False)
    CreateRichDomainModel = CreateRichDomainModel
    RichDomainModelCreated = RichDomainModelCreated
    GetA = GetA
    ProcessInbox = ProcessInbox
    ProcessOutbox = ProcessOutbox


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module"]
