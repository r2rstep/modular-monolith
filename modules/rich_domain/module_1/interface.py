from modules.rich_domain.module_1.core.application.commands.messagebox import ProcessInbox, ProcessOutbox
from modules.rich_domain.module_1.core.application.commands.rich_domain_model import CreateRichDomainModel
from modules.rich_domain.module_1.core.application.integration_events import RichDomainModelCreatedIntegrationEvent
from modules.rich_domain.module_1.core.application.queries.get_a import GetA
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from commons.message_bus.message_bus import MessageBus
from modules.rich_domain.module_1.infrastructure.container import get_container


class Module:
    message_bus = get_container().get(MessageBus)
    CreateRichDomainModel = CreateRichDomainModel
    RichDomainModelCreated: type[RichDomainModelCreated] = RichDomainModelCreated
    GetA = GetA
    ProcessInbox = ProcessInbox
    ProcessOutbox = ProcessOutbox
    RichDomainModelCreatedIntegrationEvent = RichDomainModelCreatedIntegrationEvent


def get_module() -> Module:
    return get_container().get(Module)


__all__ = ["get_module", "Module", "RichDomainModelCreated"]
