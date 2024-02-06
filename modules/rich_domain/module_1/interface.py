import injector

from modules.rich_domain.module_1.core.application.commands.rich_domain_model import CreateRichDomainModel
from modules.rich_domain.module_1.core.application.queries.get_a import GetA
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.application.message_bus import MessageBus
from modules.rich_domain.module_1.infrastructure.container import container


class Module:
    @injector.inject
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.CreateRichDomainModel = CreateRichDomainModel
        self.RichDomainModelCreated = RichDomainModelCreated
        self.GetA = GetA


def get_module() -> Module:
    return container.get(Module)


__all__ = ["get_module", "Module"]
