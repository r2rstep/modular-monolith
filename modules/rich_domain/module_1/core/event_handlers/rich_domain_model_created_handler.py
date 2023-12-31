from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.domain.events import DomainEventHandler


class RichDomainModelCreatedHandler(DomainEventHandler):
    async def handle(self, event: RichDomainModelCreated) -> None:
        ...
