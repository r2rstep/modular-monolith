from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler


class RichDomainModelCreatedHandler(DomainEventHandler[RichDomainModelCreated]):
    async def handle(self, event: RichDomainModelCreated) -> None:
        ...
